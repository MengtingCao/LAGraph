//------------------------------------------------------------------------------
// mmtest: create a matrix and test Matrix Market I/O
//------------------------------------------------------------------------------

// LAGraph, (... list all authors here) (c) 2019, All Rights Reserved.
// http://graphblas.org  See LAGraph/Doc/License.txt for license.

//------------------------------------------------------------------------------

#include "LAGraph.h"

#define OK(method)                                                          \
{                                                                           \
    GrB_Info this_info = method ;                                           \
    if (! (this_info == GrB_SUCCESS || this_info == GrB_NO_VALUE))          \
    {                                                                       \
        printf ("mmtest failure: [%d] %s\n", this_info, GrB_error ( )) ;    \
        FREE_ALL ;                                                          \
        return (this_info) ;                                                \
    }                                                                       \
}

#define FREE_ALL                    \
{                                   \
    if (f != NULL) fclose (f) ;     \
    f = NULL ;                      \
    GrB_free (&A) ;                 \
    GrB_free (&B) ;                 \
}

//------------------------------------------------------------------------------
// mmtest: create a matrix and test Matrix Market I/O
//------------------------------------------------------------------------------

GrB_Info mmtest
(
    char *filename,
    GrB_Type type,
    GrB_Index nrows,
    GrB_Index ncols,
    GrB_Index nvals,
    bool make_pattern,
    bool make_symmetric,
    bool make_skew_symmetric,
    bool make_hermitian,
    bool no_diagonal,
    uint64_t *seed
)
{
    GrB_Matrix A = NULL, B = NULL ;
    FILE *f = NULL ;

    //--------------------------------------------------------------------------
    // create a random matrix
    //--------------------------------------------------------------------------

    OK (LAGraph_random (&A, type, nrows, ncols, nvals,
        make_pattern, make_symmetric, make_skew_symmetric,
        make_hermitian, no_diagonal, seed)) ;

    // finish any pending computations
    // printf ("A random:\n") ;
    // GxB_fprint (A, GxB_COMPLETE, stdout) ;
    GrB_Matrix_nvals (&nvals, A) ;
    // printf ("A finished:\n") ;
    // GxB_fprint (A, GxB_COMPLETE, stdout) ;

    //--------------------------------------------------------------------------
    // open the output file
    //--------------------------------------------------------------------------

    f = fopen (filename, "w") ;
    if (f == NULL)
    {
        printf ("unable to create file [%s]\n", filename) ;
        FREE_ALL ;
        return (GrB_INVALID_VALUE) ;
    }

    // printf ("writing\n") ;
    // OK (LAGraph_mmwrite (A, stdout)) ;

    //--------------------------------------------------------------------------
    // write A to the file
    //--------------------------------------------------------------------------

    OK (LAGraph_mmwrite (A, f)) ;

    // printf ("wrote\n") ;

    //--------------------------------------------------------------------------
    // close the file and reopen it
    //--------------------------------------------------------------------------

    fclose (f) ;
    f = fopen (filename, "r") ;
    if (f == NULL)
    {
        printf ("unable to open file [%s]\n", filename) ;
        FREE_ALL ;
        return (GrB_INVALID_VALUE) ;
    }

    // print the first line to stderr
    /*
    char buf [1030] ;
    fgets (buf, 1030, f) ;
    fprintf (stderr, "%s", buf) ; 
    fclose (f) ;
    f = fopen (filename, "r") ;
    if (f == NULL)
    {
        printf ("unable to open file [%s]\n", filename) ;
        FREE_ALL ;
        return (GrB_INVALID_VALUE) ;
    }
    */

    //--------------------------------------------------------------------------
    // read B from the same file
    //--------------------------------------------------------------------------

    OK (LAGraph_mmread (&B, f)) ;

    // printf ("read B:\n") ;
    // GxB_fprint (B, GxB_COMPLETE, stdout) ;

    //--------------------------------------------------------------------------
    // compare the two matrices
    //--------------------------------------------------------------------------

    bool ok = false ;
    OK (LAGraph_isequal (&ok, A, B, NULL)) ;

    if (!ok)
    {
        printf ("A and B do not match\n") ;
        printf ("--------------A:\n") ;
        // GxB_fprint (A, GxB_COMPLETE, stdout) ;
        OK (LAGraph_mmwrite (A, stdout)) ;
        printf ("--------------B:\n") ;
        // GxB_fprint (B, GxB_COMPLETE, stdout) ;
        OK (LAGraph_mmwrite (B, stdout)) ;
        return (GrB_INVALID_VALUE) ;
    }

    //--------------------------------------------------------------------------
    // close file and free workspace
    //--------------------------------------------------------------------------

    FREE_ALL ;
    return (GrB_SUCCESS) ;
}

//------------------------------------------------------------------------------
// mmtest main:
//------------------------------------------------------------------------------

// calls mmtest with a huge range of combinations of matrix sizes, types,
// and characteristics.

int main (int argc, char **argv)
{

    printf ("MatrixMarket/mmtest: "
        "testing LAGraph_mmread, _mmwrite, and _random: ") ;

    LAGraph_init ( ) ;

    bool long_test = (argc > 2) ;
    printf ("%s test\n", long_test ? "long" : "short") ;

    uint64_t seed = 1 ;

    #define NTYPES 12

    GrB_Type types [NTYPES] = { GrB_BOOL,
        GrB_INT8,  GrB_INT16,  GrB_INT32,  GrB_INT64,
        GrB_UINT8, GrB_UINT16, GrB_UINT32, GrB_UINT64,
        GrB_FP32,  GrB_FP64,   LAGraph_Complex } ;

    char *typenames [NTYPES] = { "bool",
        "int8",  "int16",  "int32",  "int64",
        "uint8", "uint16", "uint32", "uint64",
        "float", "double",  "complex" } ;

    GrB_Index n1, n2, nvals1, nvals2 ;
    if (long_test)
    {
        n1 = 0 ;
        n2 = 8 ;
        nvals1 = 0 ;
        nvals2 = 30 ;
    }
    else
    {
        n1 = 6 ;
        n2 = 8 ;
        nvals1 = 29 ;
        nvals2 = 30 ;
    }

    double tic [2], t ;
    LAGraph_tic (tic) ;

    for (int k = 0 ; k < NTYPES ; k++)
    {
        printf ("%-7s: ", typenames [k]) ;
        GrB_Type type = types [k] ;
        for (GrB_Index nrows = n1 ; nrows < n2 ; nrows++)
        {
            for (GrB_Index ncols = n1 ; ncols < n2 ; ncols++)
            {
                printf (".") ;
                fflush (stdout) ;
                for (GrB_Index nvals = nvals1 ; nvals < nvals2 ; nvals++)
                {
                    for (int pat = 0 ; pat <= 1 ; pat++)
                    {
                        for (int sym = 0 ; sym <= 1 ; sym++)
                        {
                            for (int skew = 0 ; skew <= 1 ; skew++)
                            {
                                for (int herm = 0 ; herm <= 1 ; herm++)
                                {
                                    for (int nod = 0 ; nod <= 1 ; nod++)
                                    {
                                        GrB_Info info = mmtest ("A.mtx", type,
                                            nrows, ncols, nvals, pat, sym,
                                            skew, herm, nod, &seed) ;
                                        if (info != GrB_SUCCESS)
                                        {
                                            printf ("test failure: %s\n",
                                            GrB_error ( )) ;
                                            LAGraph_finalize ( ) ;
                                            abort ( ) ;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        printf ("\n") ;
    }

    t = LAGraph_toc (tic) ;
    printf ("time taken: %g sec\n", t) ;

    printf ("\nmmtest: all tests passed\n") ;
    LAGraph_finalize ( ) ;
    return (GrB_SUCCESS) ;
}

