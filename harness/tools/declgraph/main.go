// declgraph prints the top-level declarations of the given packages with their source ranges, a body-free rendering,
// and the declarations they reference, as JSON. Used by the harness to build declaration-level context slices.
//
//	declgraph -dir <module root> <import path>...
package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"go/ast"
	"go/printer"
	"go/token"
	"go/types"
	"os"
	"sort"
	"strings"

	"golang.org/x/tools/go/packages"
)

type Decl struct {
	Pkg      string   `json:"pkg"`
	Name     string   `json:"name"`
	Kind     string   `json:"kind"`
	Recv     string   `json:"recv,omitempty"`
	File     string   `json:"file"`
	Start    int      `json:"start"`
	End      int      `json:"end"`
	DocStart int      `json:"doc_start"`
	Exported bool     `json:"exported"`
	Sig      string   `json:"sig"`
	Refs     []string `json:"refs"`
}

func recvName(fd *ast.FuncDecl) string {
	if fd.Recv == nil || len(fd.Recv.List) == 0 {
		return ""
	}
	t := fd.Recv.List[0].Type
	for {
		switch x := t.(type) {
		case *ast.StarExpr:
			t = x.X
		case *ast.IndexExpr:
			t = x.X
		case *ast.IndexListExpr:
			t = x.X
		case *ast.Ident:
			return x.Name
		default:
			return ""
		}
	}
}

func objKey(obj types.Object) string {
	if obj == nil || obj.Pkg() == nil {
		return ""
	}
	if _, ok := obj.(*types.PkgName); ok {
		return ""
	}
	name := obj.Name()
	if fn, ok := obj.(*types.Func); ok {
		if sig, ok := fn.Type().(*types.Signature); ok && sig.Recv() != nil {
			rt := sig.Recv().Type()
			if p, ok := rt.(*types.Pointer); ok {
				rt = p.Elem()
			}
			if n, ok := rt.(*types.Named); ok {
				name = n.Obj().Name() + "." + name
			}
		}
	}
	if _, ok := obj.(*types.Var); ok {
		if v := obj.(*types.Var); v.IsField() {
			return ""
		}
	}
	return obj.Pkg().Path() + "." + name
}

func refs(n ast.Node, info *types.Info) []string {
	set := map[string]bool{}
	ast.Inspect(n, func(x ast.Node) bool {
		if id, ok := x.(*ast.Ident); ok {
			if k := objKey(info.Uses[id]); k != "" {
				set[k] = true
			}
		}
		return true
	})
	out := make([]string, 0, len(set))
	for k := range set {
		out = append(out, k)
	}
	sort.Strings(out)
	return out
}

func render(fset *token.FileSet, node ast.Node) string {
	var buf bytes.Buffer
	cfg := printer.Config{Mode: printer.UseSpaces | printer.TabIndent, Tabwidth: 8}
	if err := cfg.Fprint(&buf, fset, node); err != nil {
		return ""
	}
	return buf.String()
}

func main() {
	dir := flag.String("dir", ".", "module root")
	flag.Parse()
	cfg := &packages.Config{
		Mode: packages.NeedName | packages.NeedFiles | packages.NeedSyntax | packages.NeedTypes | packages.NeedTypesInfo | packages.NeedImports | packages.NeedModule,
		Dir:  *dir,
	}
	pkgs, err := packages.Load(cfg, flag.Args()...)
	if err != nil {
		fmt.Fprintln(os.Stderr, "load:", err)
		os.Exit(1)
	}
	var decls []Decl
	for _, pkg := range pkgs {
		for _, f := range pkg.Syntax {
			tf := pkg.Fset.File(f.Pos())
			fname := tf.Name()
			if pkg.Module != nil && strings.HasPrefix(fname, pkg.Module.Dir) {
				fname = strings.TrimLeft(strings.TrimPrefix(fname, pkg.Module.Dir), "/\\")
			}
			fname = strings.ReplaceAll(fname, "\\", "/")
			for _, d := range f.Decls {
				switch x := d.(type) {
				case *ast.FuncDecl:
					doc := x.Pos()
					if x.Doc != nil {
						doc = x.Doc.Pos()
					}
					cp := *x
					cp.Body = nil
					kind := "func"
					if x.Recv != nil {
						kind = "method"
					}
					decls = append(decls, Decl{Pkg: pkg.PkgPath, Name: x.Name.Name, Kind: kind, Recv: recvName(x), File: fname,
						Start: pkg.Fset.Position(x.Pos()).Line, End: pkg.Fset.Position(x.End()).Line, DocStart: pkg.Fset.Position(doc).Line,
						Exported: x.Name.IsExported(), Sig: render(pkg.Fset, &cp), Refs: refs(x, pkg.TypesInfo)})
				case *ast.GenDecl:
					if x.Tok == token.IMPORT {
						continue
					}
					doc := x.Pos()
					if x.Doc != nil {
						doc = x.Doc.Pos()
					}
					r := refs(x, pkg.TypesInfo)
					sig := render(pkg.Fset, x)
					for _, sp := range x.Specs {
						switch s := sp.(type) {
						case *ast.TypeSpec:
							decls = append(decls, Decl{Pkg: pkg.PkgPath, Name: s.Name.Name, Kind: "type", File: fname,
								Start: pkg.Fset.Position(x.Pos()).Line, End: pkg.Fset.Position(x.End()).Line, DocStart: pkg.Fset.Position(doc).Line,
								Exported: s.Name.IsExported(), Sig: sig, Refs: r})
						case *ast.ValueSpec:
							kind := "var"
							if x.Tok == token.CONST {
								kind = "const"
							}
							for _, nm := range s.Names {
								decls = append(decls, Decl{Pkg: pkg.PkgPath, Name: nm.Name, Kind: kind, File: fname,
									Start: pkg.Fset.Position(x.Pos()).Line, End: pkg.Fset.Position(x.End()).Line, DocStart: pkg.Fset.Position(doc).Line,
									Exported: nm.IsExported(), Sig: sig, Refs: r})
							}
						}
					}
				}
			}
		}
	}
	enc := json.NewEncoder(os.Stdout)
	if err := enc.Encode(map[string]any{"decls": decls, "n_pkgs": len(pkgs)}); err != nil {
		os.Exit(1)
	}
}
