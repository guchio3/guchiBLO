Title: Speeding Up Theano
Tags: Theano, Machine Learning,
Date: 2017-10-09 0:00
Modified: 2017-10-09 0:00
Slug: Speeding_Up_Theano
Authors: guchio3
Summary: Theano の速度を改良した際のメモ

# Outline
Theano の速度向上のため行ったことをメモ。

なお、使用した Theano のバージョンは 0.8.2 であり、os 情報は以下の通り。

    :::bash
    $ cat /proc/version
    Linux version 4.4.0-93-generic (buildd@lgw01-03) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #116-Ubuntu SMP Fri Aug 11 21:17:51 UTC 2017

--- 
# Profile the program
Theano には [profile 機能](http://deeplearning.net/software/theano_versions/0.8.X/tutorial/profiling.html)があり、どの部分が速度上 (他メモリ使用量なども確認できる) のボトルネックかを簡単に確認できる。  
目的によって様々な利用法があるが、私は以下のように利用した。

まず、プログラム内で 

    :::python
    theano.config.profile = True

とする。これにより theano.config が設定できる。[なお theano.config の状態は以下のコマンドで確認すれば良い。](http://deeplearning.net/software/theano_versions/0.8.X/library/config.html?highlight=profile#config.profile)

    :::bash
    $ python -c 'import theano; print(theano.config)' | less

私の場合、**系列データを扱う Neural Network **を実装しており、これの学習を扱う theano.function である train_fn が計算量のボトルネックなことが明らかだったため、[Profiling Theano function](http://deeplearning.net/software/theano_versions/0.8.X/tutorial/profiling.html) を参考に theano.function の profile.print_summary() を利用して以下のように profiling を行った。

    :::python
    print(train_fn.profile.print_summary())

以下が結果の一部。

    :::bash
    .
    .
    .

この結果より、私のプログラムの速度が遅い一番の原因は系列データを扱う際に利用している scan_fn 内において grad を計算する部分だと言うことが分かる。profile には grad_of_scan_fn の詳細も記載されており、私の場合以下のようになっていた。

    :::bash
    Scan Op profiling ( grad_of_scan_fn&grad_of_scan_fn )
    ==================
      Message: None
      Time in 100 calls of the op (for a total of 8674 steps) 2.897580e+01s
    
      Total time spent in calling the VM 2.775752e+01s (95.796%)
      Total overhead (computing slices..) 1.218287e+00s (4.204%)
    
    Class
    ---
    <% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Class name>
      18.4%    18.4%       4.680s       5.40e-05s     C    86740      10   theano.tensor.nnet.conv.ConvOp
      17.2%    35.7%       4.375s       1.26e-06s     C   3478274     401   theano.tensor.elemwise.Elemwise
      14.1%    49.8%       3.580s       2.58e-05s     Py  138784      16   theano.tensor.basic.Split
      10.2%    60.0%       2.597s       5.99e-06s     Py  433700      50   theano.tensor.blas.Dot22
       8.0%    68.0%       2.026s       1.56e-05s     Py  130110      15   theano.tensor.blas.BatchedDot
       5.1%    73.1%       1.282s       1.85e-05s     Py   69392       8   theano.tensor.blas.Gemv
       3.6%    76.7%       0.911s       1.64e-06s     C   555136      64   theano.tensor.elemwise.Sum
       3.2%    79.8%       0.811s       2.34e-05s     Py   34696       4   theano.tensor.subtensor.AdvancedIncSubtensor
       2.8%    82.6%       0.703s       2.03e-05s     C    34696       4   theano.tensor.nnet.nnet.Softmax
       2.5%    85.2%       0.643s       1.24e-05s     Py   52044       6   theano.tensor.blas.Gemm
       2.5%    87.7%       0.634s       5.22e-07s     C   1214360     140   theano.tensor.elemwise.DimShuffle
       2.2%    89.8%       0.551s       7.94e-06s     Py   69392       8   theano.tensor.blas.Dot22Scalar
       2.1%    91.9%       0.528s       5.39e-07s     C   980162     113   theano.tensor.basic.Reshape
       1.4%    93.3%       0.351s       5.47e-07s     C   641876      74   theano.tensor.subtensor.Subtensor
       1.3%    94.6%       0.339s       1.95e-05s     Py   17348       2   theano.tensor.subtensor.AdvancedSubtensor
       1.1%    95.7%       0.271s       2.08e-06s     C   130110      15   theano.tensor.basic.Join
       1.0%    96.7%       0.249s       7.18e-06s     C    34696       4   theano.tensor.subtensor.IncSubtensor
       0.5%    97.2%       0.135s       7.81e-06s     Py   17348       2   theano.tensor.basic.ARange
       0.5%    97.7%       0.131s       7.55e-06s     C    17348       2   theano.tensor.elemwise.ProdWithoutZeros
       0.4%    98.2%       0.111s       3.45e-07s     C   320938      37   theano.tensor.opt.MakeVector
       ... (remaining 8 Classes account for   1.84%(0.47s) of the runtime)
    
    Ops
    ---
    <% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Op name>
      10.2%    10.2%       2.597s       5.99e-06s     Py    433700       50   Dot22
       8.5%    18.8%       2.162s       2.49e-05s     Py    86740       10   Split{4}
       8.0%    26.7%       2.026s       1.56e-05s     Py    130110       15   BatchedDot
       7.0%    33.7%       1.777s       1.02e-04s     C     17348        2   ConvOp{('imshp', (4, 1, 128)),('kshp', (1, 128)),('nkern', 1),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'full'),('unroll_batch', 4),('unroll_kern', 1),('unroll_patch', False),('imshp_logical', (4, 1, 128)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}
       7.0%    40.7%       1.771s       1.02e-04s     C     17348        2   ConvOp{('imshp', (4, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 1),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', None),('unroll_kern', None),('unroll_patch', True),('imshp_logical', (4, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', False)}
       5.6%    46.3%       1.419s       2.73e-05s     Py    52044        6   Split{2}
       3.8%    50.1%       0.971s       2.24e-05s     Py    43370        5   Gemv{no_inplace}
       3.4%    53.6%       0.872s       1.08e-06s     C     806682       93   Elemwise{add,no_inplace}
       3.4%    56.9%       0.852s       1.20e-06s     C     711268       82   Elemwise{mul,no_inplace}
       3.2%    60.1%       0.811s       2.34e-05s     Py    34696        4   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}
       2.8%    62.9%       0.703s       2.03e-05s     C     34696        4   Softmax
       2.5%    65.4%       0.643s       1.24e-05s     Py    52044        6   Gemm{inplace}
       2.2%    67.6%       0.556s       6.41e-05s     C     8674        1   ConvOp{('imshp', (1, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', 4),('unroll_kern', 2),('unroll_patch', False),('imshp_logical', (1, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}
       2.2%    69.8%       0.551s       7.94e-06s     Py    69392        8   Dot22Scalar
       1.7%    71.4%       0.419s       1.46e-06s     C     286242       33   Sum{axis=[2], acc_dtype=float64}
       1.4%    72.9%       0.357s       2.06e-05s     C     17348        2   ConvOp{('imshp', (1, 1, 128)),('kshp', (1, 128)),('nkern', 1),('bsize', 1),('dx', 1),('dy', 1),('out_mode', 'full'),('unroll_batch', None),('unroll_kern', None),('unroll_patch', True),('imshp_logical', (1, 1, 128)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}
       1.3%    74.2%       0.339s       1.95e-05s     Py    17348        2   AdvancedSubtensor
       1.3%    75.5%       0.322s       1.24e-05s     C     26022        3   Elemwise{pow}
       1.2%    76.7%       0.311s       1.20e-05s     Py    26022        3   Gemv{inplace}
       1.2%    77.8%       0.294s       4.77e-07s     C     615854       71   Reshape{2}
       ... (remaining 112 Ops account for  22.16%(5.62s) of the runtime)
    
    Apply
    ------
    <% time> <sum %> <apply time> <time per call> <#call> <id> <Apply name>
       3.5%     3.5%       0.889s       1.02e-04s   8674   521   ConvOp{('imshp', (4, 1, 128)),('kshp', (1, 128)),('nkern', 1),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'full'),('unroll_batch', 4),('unroll_kern', 1),('unroll_patch', False),('imshp_logical', (4, 1, 128)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}(AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0, Subtensor{::, ::, ::int64, ::int64}.0)
       3.5%     7.0%       0.888s       1.02e-04s   8674   519   ConvOp{('imshp', (4, 1, 128)),('kshp', (1, 128)),('nkern', 1),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'full'),('unroll_batch', 4),('unroll_kern', 1),('unroll_patch', False),('imshp_logical', (4, 1, 128)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}(AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0, Subtensor{::, ::, ::int64, ::int64}.0)
       3.5%    10.5%       0.886s       1.02e-04s   8674   543   ConvOp{('imshp', (4, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 1),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', None),('unroll_kern', None),('unroll_patch', True),('imshp_logical', (4, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', False)}(InplaceDimShuffle{1,0,2,3}.0, Subtensor{::, ::, ::int64, ::int64}.0)
       3.5%    14.0%       0.885s       1.02e-04s   8674   545   ConvOp{('imshp', (4, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 1),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', None),('unroll_kern', None),('unroll_patch', True),('imshp_logical', (4, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', False)}(InplaceDimShuffle{1,0,2,3}.0, Subtensor{::, ::, ::int64, ::int64}.0)
       2.2%    16.2%       0.556s       6.41e-05s   8674   441   ConvOp{('imshp', (1, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', 4),('unroll_kern', 2),('unroll_patch', False),('imshp_logical', (1, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}(Subtensor{::, ::, ::, :int64:}.0, Elemwise{mul,no_inplace}.0)
       1.6%    17.8%       0.405s       4.67e-05s   8674   738   Dot22(InplaceDimShuffle{1,0}.0, Reshape{2}.0)
       1.6%    19.4%       0.404s       4.65e-05s   8674   824   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
       1.3%    20.7%       0.334s       3.86e-05s   8674   428   Softmax(Reshape{2}.0)
       1.0%    21.7%       0.264s       3.04e-05s   8674   903   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
       1.0%    22.7%       0.259s       2.98e-05s   8674   854   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
       1.0%    23.8%       0.258s       2.98e-05s   8674   573   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
       1.0%    24.7%       0.245s       2.82e-05s   8674   224   Gemv{no_inplace}(InplaceDimShuffle{1}.0, TensorConstant{1.0}, controller.W_in_and_reads_to_o_copy01.T, InplaceDimShuffle{1}.0, TensorConstant{1.0})
       0.9%    25.7%       0.240s       2.77e-05s   8674   602   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
       0.9%    26.6%       0.236s       2.72e-05s   8674   427   Softmax(Reshape{2}.0)
       0.9%    27.5%       0.235s       2.71e-05s   8674   577   Split{2}(IncSubtensor{InplaceInc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
       0.9%    28.4%       0.231s       2.67e-05s   8674   1002   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
       0.9%    29.3%       0.230s       2.65e-05s   8674   1001   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
       0.9%    30.2%       0.226s       2.61e-05s   8674   512   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(4, 4, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
       0.9%    31.1%       0.224s       2.59e-05s   8674   609   Split{2}(IncSubtensor{InplaceInc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
       0.9%    32.0%       0.218s       2.51e-05s   8674   511   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(4, 4, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
       ... (remaining 1079 Apply instances account for 68.03%(17.26s) of the runtime)
    
    Here are tips to potentially make your code run faster
                     (if you think of new ones, suggest them on the mailing list).
                     Test them first, as they are not guaranteed to always provide a speedup.
      - Try installing amdlibm and set the Theano flag lib.amdlibm=True. This speeds up only some Elemwise operation.

以上の結果から、プログラムの速度を向上を図るために以下の２つの試みを行ってみた。

0. Theano の blas 環境整備
    * theano.tensor.blas.~ 系が <type> Py となっており、これは numpy を介して openblas を使用している？ようなのでこれの改良が可能？
0. amdlibm (?) のインストール
    * 上記の profile の最後にかかれているように、これにより Elemwise operation (17.2% とボトルネックの一つになっている) を改善できそう。


--- 
# blas environment setting
### motivation
上記の通り、theano.tensor.blas.~ 系が <type> Py となっている。[環境によっては同様の演算が <type> C で行われるらしく](https://groups.google.com/forum/#!searchin/theano-users/Gemv%7Csort:date/theano-users/UfPNnTI1pI4/2w48Gid_BwAJ)、ググったところ[これは theano の BLAS の設定に起因していそう](https://groups.google.com/forum/#!topic/theano-users/9JdhCfp4YFM)。  

そこで設定を以下のコマンドにより確認したところの出力が None だった (何も出力されない) ため、theano.config.blas.ldflags が設定されていないことがわかる。

    :::bash
    $ python -c "import theano; print(theano.config.blas.ldflags)"

[公式ドキュメント](http://deeplearning.net/software/theano_versions/0.8.X/install_ubuntu.html)によると (Speed test Theano/BLAS 参照) Theano は theano.config.blas.ldflags が未設定の場合 Numpy/Scipy を介して BLAS を利用するが、これにより生じるオーバーヘッドが今回の profile でボトルネックの１つとなっている theano.tensor.blas.Gemm や theano.tensor.blas.Dot において重要らしい。

ちなみに、使用している Numpy の blas は以下のように openblas だった。

    :::bash
    $ python -c "import numpy as np; print(np.__config__.show())"
    lapack_opt_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        define_macros = [('HAVE_CBLAS', None)]
        language = c
    blas_opt_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        define_macros = [('HAVE_CBLAS', None)]
        language = c
    openblas_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        define_macros = [('HAVE_CBLAS', None)]
        language = c
    blis_info:
      NOT AVAILABLE
    openblas_lapack_info:
        libraries = ['openblas', 'openblas']
        library_dirs = ['/usr/local/lib']
        define_macros = [('HAVE_CBLAS', None)]
        language = c
    lapack_mkl_info:
      NOT AVAILABLE
    blas_mkl_info:
      NOT AVAILABLE
    None

[Qiita の記事](https://qiita.com/unnonouno/items/8ab453a1868d77a93679)によると openblas から [intel の mkl](https://software.intel.com/en-us/articles/getting-started-with-intel-optimized-theano) へと変更することで Chainer の性能が約 1.5 になるらしいのでこれを blas として利用することにした。


### install mkl (and setting new environment)
[intel のダウンロードサイト](https://software.intel.com/en-us/mkl)の Free Download から簡単に個人情報登録し、mkl をダウンロードした。  
私の場合は l_mkl_2018.0.128.tgz というファイルがダウンロードされ、これを Ubuntu 上で展開した。  
後は l_mkl_2018.0.128/install.sh を走らせると対話型のインストールが行えるため、流れに沿っていれば良い。

なお、ユーザアカウントでこれを行った場合、root ユーザとしてインストールをする (システム上の全ユーザが使えるようにする) かローカル環境にダウンロードするか選べるが、前者の場合は /opt/ 以下に、後者の場合は ~/ 以下にそれぞれ intel/ というディレクトリが作られ、その下にインストールが行われる。

...と、ここまで mkl インストールしてきたが、[Theanoの公式](http://deeplearning.net/software/theano/install_ubuntu.html)に mkl を使う場合 conda を使って環境設定を行えば良いと書いてあるので、今まで pip を使用して作っていた環境を conda を利用して作ることにした。 

conda を用い、以下のコマンドを入力。

    :::bash
    $ conda install numpy scipy mkl

すると以下のエラーが出た。

    :::bash
    ERROR conda.core.link:_execute_actions(337): An error occurred while installing package 'defaults::numpy-1.13.3-py27hbcc08e0_0'.
    CondaError: Cannot link a source that does not exist. /home/guchio/miniconda2/pkgs/numpy-1.13.3-py27hbcc08e0_0/bin/f2py
    Attempting to roll back.


    CondaError: Cannot link a source that does not exist. /home/guchio/miniconda2/pkgs/numpy-1.13.3-py27hbcc08e0_0/bin/f2py

そこで[ここ](https://github.com/conda/conda/issues/6078)を参考に、以下を行ったところ解決。

    :::bash
    $ conda clean --all
    $ conda update conda
    $ conda update --all

これで以下のように conda 上に mkl を利用する numpy の実行環境が完成。  

	:::bash
	$ python -c "import numpy as np; print(np.__config__.show())"
	lapack_opt_info:
	    libraries = ['mkl_rt', 'pthread']
	    library_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/lib']
	    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
	    include_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/include']
	blas_opt_info:
	    libraries = ['mkl_rt', 'pthread']
	    library_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/lib']
	    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
	    include_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/include']
	lapack_mkl_info:
	    libraries = ['mkl_rt', 'pthread']
	    library_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/lib']
	    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
	    include_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/include']
	blas_mkl_info:
	    libraries = ['mkl_rt', 'pthread']
	    library_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/lib']
	    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
	    include_dirs = ['/home/guchio/miniconda2/envs/ntmenv-owl/include']
	None

そこで、openblas を利用した場合と mkl を利用した場合の速度テストを以下のコードによって行ってみた。

	:::python
	import numpy as np
	import time
	
	a = np.array(np.arange(4000000).reshape(2000, 2000))
	b = np.array(np.arange(4000000).reshape(2000, 2000))
	
	before_time = time.clock()
	np.dot(a, b)
	after_time = time.clock()
	print(after_time - before_time)

結果は openblas を利用するものが 25.502314、mkl を利用するものが 21.625779 となった。

次に Theano も以下のように入れ直し、無事成功。

	:::bash
	$ conda install theano=0.8.2
    $ python -c "import theano; print(theano.config.blas.ldflags)"
	-L/home/guchio/miniconda2/envs/ntmenv-owl/lib -lmkl_rt -lpthread -lm -lm

Theano の速度テストをしてみる。

	:::bash
	$ python `python -c "import os, theano; print(os.path.dirname(theano.__file__))"`/misc/check_blas.py

結果は numpy 経由で openblas を利用するものが 11.99s、mkl を利用するものが 11.32s となった。  
正直あまり変わらない...

### Result
環境も整ったので profiling してみた。以下が結果。


# aa
[ここ](http://developer.amd.com/amd-cpu-libraries/amd-math-library-libm/)からダウンロード
[ここ](https://hvasbath.github.io/beat/installation.html)を参考にインストールした。
