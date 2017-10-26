Title: Speeding Up Theano
Tags: Theano, Machine Learning,
Date: 2017-10-10 19:00
Modified: 2017-10-21 14:00
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

以下が結果の一部。

    :::bash
	Function profiling
	==================
	  Message: examples/run_tasks.py:376
	  Time in 100 calls to Function.__call__: 5.591766e+01s
	  Time in Function.fn.__call__: 5.585304e+01s (99.884%)
	  Time in thunks: 5.549018e+01s (99.236%)
	  Total compile time: 9.343460e+02s
	    Number of Apply nodes: 1288
	    Theano Optimizer time: 8.834189e+02s
	       Theano validate time: 2.949661e+00s
	    Theano Linker time (includes C, CUDA code generation/compiling): 4.475670e+01s
	       Import time 3.738601e-01s
	
	Time in all call to theano.grad() 2.802125e+01s
	Time since theano import 1045.185s
	Class
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Class name>
	  99.0%    99.0%      54.942s       2.75e-01s     Py     200       2   theano.scan_module.scan_op.Scan
	   0.4%    99.5%       0.243s       3.55e-06s     C    68500     685   theano.tensor.elemwise.Elemwise
	   0.2%    99.6%       0.095s       9.54e-05s     Py    1000      10   theano.tensor.blas.Dot22
	   0.1%    99.7%       0.053s       6.93e-06s     C     7600      76   theano.tensor.basic.Alloc
	   0.1%    99.8%       0.033s       3.25e-04s     C      100       1   theano.tensor.nnet.nnet.SoftmaxWithBias
	   0.1%    99.8%       0.028s       9.45e-05s     Py     300       3   theano.tensor.blas.Gemm
	   0.0%    99.9%       0.014s       7.81e-07s     C    17300     173   theano.compile.ops.Shape_i
	   0.0%    99.9%       0.011s       8.60e-06s     C     1300      13   theano.tensor.basic.Join
	   0.0%    99.9%       0.010s       2.72e-06s     C     3600      36   theano.tensor.basic.Reshape
	   0.0%    99.9%       0.010s       1.19e-05s     C      800       8   theano.tensor.subtensor.IncSubtensor
	   0.0%    99.9%       0.008s       1.13e-06s     C     7500      75   theano.tensor.subtensor.Subtensor
	   0.0%    99.9%       0.007s       1.03e-06s     C     7100      71   theano.tensor.elemwise.DimShuffle
	   0.0%    99.9%       0.006s       3.20e-05s     Py     200       2   theano.tensor.subtensor.AdvancedSubtensor
	   0.0%   100.0%       0.006s       7.98e-07s     C     7700      77   theano.tensor.opt.MakeVector
	   0.0%   100.0%       0.006s       5.55e-05s     Py     100       1   theano.tensor.subtensor.AdvancedIncSubtensor
	   0.0%   100.0%       0.004s       3.89e-05s     Py     100       1   theano.tensor.basic.Nonzero
	   0.0%   100.0%       0.004s       3.73e-05s     C      100       1   theano.tensor.nnet.nnet.SoftmaxGrad
	   0.0%   100.0%       0.003s       1.69e-05s     C      200       2   theano.tensor.subtensor.AdvancedSubtensor1
	   0.0%   100.0%       0.003s       6.30e-06s     C      400       4   theano.tensor.elemwise.Sum
	   0.0%   100.0%       0.001s       6.83e-07s     C     1700      17   theano.tensor.basic.ScalarFromTensor
	   ... (remaining 5 Classes account for   0.01%(0.00s) of the runtime)
	
	Ops
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Op name>
	  87.7%    87.7%      48.643s       4.86e-01s     Py     100        1   forall_inplace,cpu,grad_of_scan_fn&grad_of_scan_fn}
	  11.4%    99.0%       6.300s       6.30e-02s     Py     100        1   forall_inplace,cpu,scan_fn}
	   0.2%    99.2%       0.095s       9.54e-05s     Py    1000       10   Dot22
	   0.1%    99.3%       0.053s       6.93e-06s     C     7600       76   Alloc
	   0.1%    99.3%       0.033s       5.49e-06s     C     6000       60   Elemwise{Clip}[(0, 0)]
	   0.1%    99.4%       0.033s       3.25e-04s     C      100        1   SoftmaxWithBias
	   0.1%    99.4%       0.029s       2.56e-06s     C     11300      113   Elemwise{Add}[(0, 0)]
	   0.1%    99.5%       0.028s       9.45e-05s     Py     300        3   Gemm{inplace}
	   0.1%    99.6%       0.028s       4.77e-06s     C     5900       59   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)]
	   0.0%    99.6%       0.024s       4.11e-06s     C     5900       59   Elemwise{Composite{((i0 * i1) + (i2 * i3))}}
	   0.0%    99.6%       0.020s       2.91e-06s     C     7000       70   Elemwise{Mul}[(0, 1)]
	   0.0%    99.7%       0.020s       1.95e-04s     C      100        1   Elemwise{sqr,no_inplace}
	   0.0%    99.7%       0.019s       2.74e-06s     C     7000       70   Elemwise{Composite{(i0 * sqr(i1))}}
	   0.0%    99.7%       0.018s       2.83e-06s     C     6200       62   Elemwise{add,no_inplace}
	   0.0%    99.8%       0.011s       8.60e-06s     C     1300       13   Join
	   0.0%    99.8%       0.011s       1.33e-05s     C      800        8   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}
	   0.0%    99.8%       0.009s       3.28e-06s     C     2700       27   Reshape{2}
	   0.0%    99.8%       0.008s       6.85e-06s     C     1100       11   Elemwise{clip,no_inplace}
	   0.0%    99.8%       0.007s       9.06e-07s     C     7500       75   Shape_i{0}
	   0.0%    99.8%       0.007s       6.60e-05s     C      100        1   IncSubtensor{Inc;:int64:}
	   ... (remaining 109 Ops account for   0.17%(0.10s) of the runtime)
	
	Apply
	------
	<% time> <sum %> <apply time> <time per call> <#call> <id> <Apply name>
	  87.7%    87.7%      48.643s       4.86e-01s    100   783   forall_inplace,cpu,grad_of_scan_fn&grad_of_scan_fn}(Elemwise{Composite{Switch(EQ(i0, i1), ((i2 * i3) // (i4 * i0)), i0)}}.	0, Elemwise{sqr,no_inplace}.0, InplaceDimShuffle{0,1,3,2}.0, InplaceDimShuffle{0,1,3,2}.0, InplaceDimShuffle{0,1,2}.0, InplaceDimShuffle{0,1,2,3,x}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int6
	  11.4%    99.0%       6.300s       6.30e-02s    100   688   forall_inplace,cpu,scan_fn}(Elemwise{Composite{Switch(EQ(i0, i1), ((i2 * i3) // (i4 * i0)), i0)}}.0, Subtensor{int64:int64:int8}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, controller.W_in_and_reads_to_o01, controller.W_hid_to_o01, controller.W_in_and_reads_to_i01, controller.W_hid_to_i01, controller.W_in_and_rea
	   0.1%    99.1%       0.033s       3.25e-04s    100   723   SoftmaxWithBias(Dot22.0, output_modality_net.b)
	   0.0%    99.1%       0.020s       1.95e-04s    100   733   Elemwise{sqr,no_inplace}(Subtensor{int64:int64:int64}.0)
	   0.0%    99.1%       0.014s       1.42e-04s    100   716   Dot22(Reshape{2}.0, output_modality_net.W)
	   0.0%    99.2%       0.012s       1.18e-04s    100   907   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.2%       0.012s       1.17e-04s    100   764   Dot22(InplaceDimShuffle{1,0}.0, SoftmaxGrad.0)
	   0.0%    99.2%       0.011s       1.11e-04s    100   912   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.2%       0.011s       1.07e-04s    100   765   Dot22(SoftmaxGrad.0, output_modality_net.W.T)
	   0.0%    99.2%       0.011s       1.05e-04s    100   491   Alloc(TensorConstant{0.0}, Elemwise{add,no_inplace}.0, TensorConstant{1}, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.	0, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0)
	   0.0%    99.3%       0.010s       1.05e-04s    100   487   Alloc(TensorConstant{0.0}, Elemwise{add,no_inplace}.0, TensorConstant{1}, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0)
	   0.0%    99.3%       0.010s       1.04e-04s    100   1236   Gemm{inplace}(Alloc.0, TensorConstant{1.0}, Reshape{2}.0, Reshape{2}.0, TensorConstant{1.0})
	   0.0%    99.3%       0.009s       9.34e-05s    100   1237   Gemm{inplace}(Alloc.0, TensorConstant{1.0}, Reshape{2}.0, Reshape{2}.0, TensorConstant{1.0})
	   0.0%    99.3%       0.009s       9.30e-05s    100   914   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.3%       0.009s       9.14e-05s    100   916   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.3%       0.009s       8.63e-05s    100   1238   Gemm{inplace}(Alloc.0, TensorConstant{1.0}, Reshape{2}.0, Reshape{2}.0, TensorConstant{1.0})
	   0.0%    99.3%       0.007s       7.35e-05s    100   1103   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.4%       0.007s       6.60e-05s    100   918   IncSubtensor{Inc;:int64:}(Alloc.0, Subtensor{::int64}.0, ScalarFromTensor.0)
	   0.0%    99.4%       0.006s       6.28e-05s    100   1257   Dot22(InplaceDimShuffle{1,0}.0, Elemwise{Composite{((i0 * i1) + (i0 * i1 * sgn(i2)))}}[(0, 1)].0)
	   0.0%    99.4%       0.006s       5.62e-05s    100    74   Join(TensorConstant{0}, read0.read0.shift.W, read1.read1.shift.W, read2.read2.shift.W, read3.read3.shift.W)
	   ... (remaining 1268 Apply instances account for 0.62%(0.34s) of the runtime)
	
	Here are tips to potentially make your code run faster
	                 (if you think of new ones, suggest them on the mailing list).
	                 Test them first, as they are not guaranteed to always provide a speedup.
	  - Try installing amdlibm and set the Theano flag lib.amdlibm=True. This speeds up only some Elemwise operation.
	
	    .
	    .
	    .

この結果より、私のプログラムの速度が遅い一番の原因は系列データを扱う際に利用している scan_fn 内において grad を計算する部分だと言うことが分かる。profile には grad_of_scan_fn の詳細も記載されており、私の場合以下のようになっていた。

	:::bash
	Scan Op profiling ( grad_of_scan_fn&grad_of_scan_fn )
	==================
	  Message: None
	  Time in 100 calls of the op (for a total of 8671 steps) 4.828692e+01s
	
	  Total time spent in calling the VM 4.562579e+01s (94.489%)
	  Total overhead (computing slices..) 2.661133e+00s (5.511%)
	
	Class
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Class name>
	  20.5%    20.5%       8.227s       2.43e-06s     C   3390361     391   theano.tensor.elemwise.Elemwise
	  13.1%    33.7%       5.250s       6.05e-05s     C    86710      10   theano.tensor.nnet.conv.ConvOp
	  13.1%    46.7%       5.229s       1.21e-05s     Py  433550      50   theano.tensor.blas.Dot22
	  12.4%    59.2%       4.985s       3.59e-05s     Py  138736      16   theano.tensor.basic.Split
	   7.3%    66.4%       2.914s       2.24e-05s     Py  130065      15   theano.tensor.blas.BatchedDot
	   4.8%    71.2%       1.914s       2.76e-05s     Py   69368       8   theano.tensor.blas.Gemv
	   3.6%    74.8%       1.433s       1.18e-06s     C   1213940     140   theano.tensor.elemwise.DimShuffle
	   3.4%    78.2%       1.379s       2.48e-06s     C   554944      64   theano.tensor.elemwise.Sum
	   3.1%    81.3%       1.235s       1.26e-06s     C   979823     113   theano.tensor.basic.Reshape
	   3.0%    84.3%       1.191s       2.29e-05s     Py   52026       6   theano.tensor.blas.Gemm
	   2.8%    87.1%       1.105s       3.19e-05s     Py   34684       4   theano.tensor.subtensor.AdvancedIncSubtensor
	   2.7%    89.8%       1.097s       1.58e-05s     Py   69368       8   theano.tensor.blas.Dot22Scalar
	   1.7%    91.5%       0.689s       1.07e-06s     C   641654      74   theano.tensor.subtensor.Subtensor
	   1.2%    92.7%       0.476s       2.74e-05s     Py   17342       2   theano.tensor.subtensor.AdvancedSubtensor
	   1.1%    93.8%       0.439s       3.38e-06s     C   130065      15   theano.tensor.basic.Join
	   0.9%    94.7%       0.349s       9.57e-07s     C   364182      42   theano.compile.ops.Shape_i
	   0.9%    95.5%       0.347s       9.99e-06s     C    34684       4   theano.tensor.subtensor.IncSubtensor
	   0.8%    96.4%       0.339s       9.77e-06s     C    34684       4   theano.tensor.nnet.nnet.Softmax
	   0.7%    97.1%       0.286s       8.90e-07s     C   320827      37   theano.tensor.opt.MakeVector
	   0.6%    97.7%       0.229s       1.32e-05s     Py   17342       2   theano.tensor.basic.ARange
	   ... (remaining 8 Classes account for   2.33%(0.93s) of the runtime)
	
	Ops
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Op name>
	  13.1%    13.1%       5.229s       1.21e-05s     Py    433550       50   Dot22
	   7.8%    20.8%       3.118s       3.60e-05s     Py    86710       10   Split{4}
	   7.3%    28.1%       2.914s       2.24e-05s     Py    130065       15   BatchedDot
	   4.8%    32.9%       1.928s       1.11e-04s     C     17342        2   ConvOp{('imshp', (4, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 1),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', None),('unroll_kern', None),('unroll_patch', True),('imshp_logical', (4, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', False)}
	   4.8%    37.7%       1.903s       1.10e-04s     C     17342        2   ConvOp{('imshp', (4, 1, 128)),('kshp', (1, 128)),('nkern', 1),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'full'),('unroll_batch', 4),('unroll_kern', 1),('unroll_patch', False),('imshp_logical', (4, 1, 128)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}
	   4.7%    42.3%       1.867s       3.59e-05s     Py    52026        6   Split{2}
	   4.4%    46.8%       1.775s       2.44e-06s     C     728364       84   Elemwise{mul,no_inplace}
	   4.3%    51.1%       1.717s       2.42e-06s     C     711022       82   Elemwise{add,no_inplace}
	   3.4%    54.4%       1.352s       3.12e-05s     Py    43355        5   Gemv{no_inplace}
	   3.0%    57.4%       1.191s       2.29e-05s     Py    52026        6   Gemm{inplace}
	   2.8%    60.2%       1.105s       3.19e-05s     Py    34684        4   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}
	   2.7%    62.9%       1.097s       1.58e-05s     Py    69368        8   Dot22Scalar
	   1.9%    64.8%       0.753s       8.68e-05s     C     8671        1   ConvOp{('imshp', (1, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'va	lid'),('unroll_batch', 4),('unroll_kern', 2),('unroll_patch', False),('imshp_logical', (1, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}
	   1.8%    66.6%       0.707s       1.15e-06s     C     615641       71   Reshape{2}
	   1.6%    68.2%       0.637s       2.23e-06s     C     286143       33   Sum{axis=[2], acc_dtype=float64}
	   1.4%    69.6%       0.562s       2.16e-05s     Py    26013        3   Gemv{inplace}
	   1.3%    70.9%       0.532s       9.89e-07s     C     537602       62   Subtensor{int64}
	   1.3%    72.2%       0.528s       1.45e-06s     C     364182       42   Reshape{3}
	   1.2%    73.4%       0.476s       2.74e-05s     Py    17342        2   AdvancedSubtensor
	   1.1%    74.5%       0.439s       3.38e-06s     C     130065       15   Join
	   ... (remaining 113 Ops account for  25.51%(10.22s) of the runtime)
	
	Apply
	------
	<% time> <sum %> <apply time> <time per call> <#call> <id> <Apply name>
	   2.4%     2.4%       0.969s       1.12e-04s   8671   545   ConvOp{('imshp', (4, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 1),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', None),('unroll_kern', None),('unroll_patch', True),('imshp_logical', (4, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', False)}(InplaceDimShuffle{1,0,2,3}.0, Subtensor{::, ::, ::int64, ::int64}.0)
	   2.4%     4.8%       0.958s       1.11e-04s   8671   543   ConvOp{('imshp', (4, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 1),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', None),('unroll_kern', None),('unroll_patch', True),('imshp_logical', (4, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', False)}(InplaceDimShuffle{1,0,2,3}.0, Subtensor{::, ::, ::int64, ::int64}.0)
	   2.4%     7.2%       0.952s       1.10e-04s   8671   521   ConvOp{('imshp', (4, 1, 128)),('kshp', (1, 128)),('nkern', 1),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'full'),('unroll_batch', 4),('unroll_kern', 1),('unroll_patch', False),('imshp_logical', (4, 1, 128)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}(AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0, Subtensor{::, ::, ::int64, ::int64}.0)
	   2.4%     9.6%       0.950s       1.10e-04s   8671   519   ConvOp{('imshp', (4, 1, 128)),('kshp', (1, 128)),('nkern', 1),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'full'),('unroll_batch', 4),('unroll_kern', 1),('unroll_patch', False),('imshp_logical', (4, 1, 128)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}(AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0, Subtensor{::, ::, ::int64, ::int64}.0)
	   1.9%    11.4%       0.753s       8.68e-05s   8671   441   ConvOp{('imshp', (1, 1, 255)),('kshp', (1, 128)),('nkern', 4),('bsize', 4),('dx', 1),('dy', 1),('out_mode', 'valid'),('unroll_batch', 4),('unroll_kern', 2),('unroll_patch', False),('imshp_logical', (1, 1, 255)),('kshp_logical', (1, 128)),('kshp_logical_top_aligned', True)}(Subtensor{::, ::, ::, :int64:}.0, Elemwise{mul,no_inplace}.0)
	   1.8%    13.3%       0.731s       8.43e-05s   8671   825   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   1.7%    15.0%       0.686s       7.91e-05s   8671   737   Dot22(InplaceDimShuffle{1,0}.0, Reshape{2}.0)
	   1.0%    16.0%       0.410s       4.73e-05s   8671   573   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   1.0%    17.0%       0.396s       4.57e-05s   8671   893   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   0.9%    17.9%       0.367s       4.24e-05s   8671   843   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   0.9%    18.8%       0.357s       4.12e-05s   8671   224   Gemv{no_inplace}(InplaceDimShuffle{1}.0, TensorConstant{1.0}, controller.W_in_and_reads_to_o_copy01.T, InplaceDimShuffle{1}.0, TensorConstant{1.0})
	   0.8%    19.6%       0.312s       3.60e-05s   8671   739   Dot22(Reshape{2}.0, <TensorType(float32, matrix)>)
	   0.8%    20.3%       0.304s       3.51e-05s   8671   527   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(1, 1, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   0.8%    21.1%       0.301s       3.47e-05s   8671   511   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(4, 4, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   0.7%    21.8%       0.297s       3.43e-05s   8671   601   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   0.7%    22.6%       0.297s       3.42e-05s   8671   577   Split{2}(IncSubtensor{InplaceInc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   0.7%    23.3%       0.295s       3.41e-05s   8671   992   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
	   0.7%    24.1%       0.295s       3.40e-05s   8671   736   Dot22(Reshape{2}.0, <TensorType(float32, matrix)>)
	   0.7%    24.8%       0.293s       3.38e-05s   8671   317   Dot22(Reshape{2}.0, <TensorType(float32, matrix)>)
	   0.7%    25.5%       0.291s       3.36e-05s   8671   991   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
	   ... (remaining 1069 Apply instances account for 74.49%(29.83s) of the runtime)
	
	Here are tips to potentially make your code run faster
	                 (if you think of new ones, suggest them on the mailing list).
	                 Test them first, as they are not guaranteed to always provide a speedup.
	  - Try installing amdlibm and set the Theano flag lib.amdlibm=True. This speeds up only some Elemwise operation.

以上の結果から、プログラムの速度を向上を図るために以下の２つの試みを行ってみた。

0. Theano の blas 環境整備
    * theano.tensor.blas.~ 系が <type> Py となっており、これは numpy を介して openblas を使用している？ようなのでこれの改良が可能？
0. amdlibm のインストール
    * 上記の profile の最後にかかれているように、これにより Elemwise operation (20.5% とボトルネックの一つになっている) を改善できそう。


--- 
# Blas environment setting
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


### Install mkl (and setting new environment)
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

	:::bash
	Function profiling
	==================
	  Message: examples/run_tasks.py:376
	  Time in 100 calls to Function.__call__: 4.939490e+01s
	  Time in Function.fn.__call__: 4.933104e+01s (99.871%)
	  Time in thunks: 4.895610e+01s (99.112%)
	  Total compile time: 1.077718e+03s
	    Number of Apply nodes: 1288
	    Theano Optimizer time: 1.013889e+03s
	       Theano validate time: 3.349193e+00s
	    Theano Linker time (includes C, CUDA code generation/compiling): 5.913572e+01s
	       Import time 7.540491e-01s
	
	Time in all call to theano.grad() 3.068751e+01s
	Time since theano import 1184.741s
	Class
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Class name>
	  98.9%    98.9%      48.411s       2.42e-01s     Py     200       2   theano.scan_module.scan_op.Scan
	   0.5%    99.4%       0.260s       3.79e-06s     C    68500     685   theano.tensor.elemwise.Elemwise
	   0.2%    99.6%       0.076s       7.57e-05s     C     1000      10   theano.tensor.blas.Dot22
	   0.1%    99.7%       0.056s       7.38e-06s     C     7600      76   theano.tensor.basic.Alloc
	   0.1%    99.7%       0.031s       3.08e-04s     C      100       1   theano.tensor.nnet.nnet.SoftmaxWithBias
	   0.0%    99.8%       0.016s       5.26e-05s     C      300       3   theano.tensor.blas.Gemm
	   0.0%    99.8%       0.013s       7.60e-07s     C    17300     173   theano.compile.ops.Shape_i
	   0.0%    99.8%       0.012s       1.52e-05s     C      800       8   theano.tensor.subtensor.IncSubtensor
	   0.0%    99.9%       0.012s       9.10e-06s     C     1300      13   theano.tensor.basic.Join
	   0.0%    99.9%       0.011s       2.94e-06s     C     3600      36   theano.tensor.basic.Reshape
	   0.0%    99.9%       0.009s       4.69e-05s     Py     200       2   theano.tensor.subtensor.AdvancedSubtensor
	   0.0%    99.9%       0.009s       1.15e-06s     C     7500      75   theano.tensor.subtensor.Subtensor
	   0.0%    99.9%       0.008s       1.09e-06s     C     7100      71   theano.tensor.elemwise.DimShuffle
	   0.0%    99.9%       0.007s       7.10e-05s     Py     100       1   theano.tensor.subtensor.AdvancedIncSubtensor
	   0.0%   100.0%       0.007s       8.76e-07s     C     7700      77   theano.tensor.opt.MakeVector
	   0.0%   100.0%       0.005s       4.84e-05s     Py     100       1   theano.tensor.basic.Nonzero
	   0.0%   100.0%       0.004s       3.68e-05s     C      100       1   theano.tensor.nnet.nnet.SoftmaxGrad
	   0.0%   100.0%       0.003s       1.59e-05s     C      200       2   theano.tensor.subtensor.AdvancedSubtensor1
	   0.0%   100.0%       0.003s       7.57e-06s     C      400       4   theano.tensor.elemwise.Sum
	   0.0%   100.0%       0.001s       1.35e-05s     C      100       1   theano.compile.ops.DeepCopyOp
	   ... (remaining 5 Classes account for   0.01%(0.00s) of the runtime)
	
	Ops
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Op name>
	  89.8%    89.8%      43.985s       4.40e-01s     Py     100        1   forall_inplace,cpu,grad_of_scan_fn&grad_of_scan_fn}
	   9.0%    98.9%       4.426s       4.43e-02s     Py     100        1   forall_inplace,cpu,scan_fn}
	   0.2%    99.0%       0.076s       7.57e-05s     C     1000       10   Dot22
	   0.1%    99.2%       0.056s       7.38e-06s     C     7600       76   Alloc
	   0.1%    99.2%       0.034s       5.62e-06s     C     6000       60   Elemwise{Clip}[(0, 0)]
	   0.1%    99.3%       0.031s       3.08e-04s     C      100        1   SoftmaxWithBias
	   0.1%    99.3%       0.030s       2.68e-06s     C     11300      113   Elemwise{Add}[(0, 0)]
	   0.1%    99.4%       0.029s       4.97e-06s     C     5900       59   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)]
	   0.1%    99.5%       0.026s       4.39e-06s     C     5900       59   Elemwise{Composite{((i0 * i1) + (i2 * i3))}}
	   0.0%    99.5%       0.023s       3.25e-06s     C     7000       70   Elemwise{Mul}[(0, 1)]
	   0.0%    99.6%       0.021s       2.07e-04s     C      100        1   Elemwise{sqr,no_inplace}
	   0.0%    99.6%       0.020s       2.91e-06s     C     7000       70   Elemwise{Composite{(i0 * sqr(i1))}}
	   0.0%    99.6%       0.019s       3.04e-06s     C     6200       62   Elemwise{add,no_inplace}
	   0.0%    99.7%       0.016s       5.26e-05s     C      300        3   Gemm{inplace}
	   0.0%    99.7%       0.012s       1.48e-05s     C      800        8   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}
	   0.0%    99.7%       0.012s       9.10e-06s     C     1300       13   Join
	   0.0%    99.7%       0.010s       3.52e-06s     C     2700       27   Reshape{2}
	   0.0%    99.8%       0.009s       4.69e-05s     Py     200        2   AdvancedSubtensor
	   0.0%    99.8%       0.008s       8.38e-05s     C      100        1   IncSubtensor{Inc;:int64:}
	   0.0%    99.8%       0.008s       7.00e-06s     C     1100       11   Elemwise{clip,no_inplace}
	   ... (remaining 109 Ops account for   0.22%(0.11s) of the runtime)
	
	Apply
	------
	<% time> <sum %> <apply time> <time per call> <#call> <id> <Apply name>
	  89.8%    89.8%      43.985s       4.40e-01s    100   783   forall_inplace,cpu,grad_of_scan_fn&grad_of_scan_fn}(Elemwise{Composite{Switch(EQ(i0, i1), ((i2 * i3) // (i4 * i0)), i0)}}.0, Elemwise{sqr,no_inplace}.0, InplaceDimShuffle{0,1,3,2}.0, InplaceDimShuffle{0,1,3,2}.0, InplaceDimShuffle{0,1,2}.0, InplaceDimShuffle{0,1,2,3,x}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int6
	   9.0%    98.9%       4.426s       4.43e-02s    100   688   forall_inplace,cpu,scan_fn}(Elemwise{Composite{Switch(EQ(i0, i1), ((i2 * i3) // (i4 * i0)), i0)}}.0, Subtensor{int64:int64:int8}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, controller.W_in_and_reads_to_o01, controller.W_hid_to_o01, controller.W_in_and_reads_to_i01, controller.W_hid_to_i01, controller.W_in_and_rea
	   0.1%    99.0%       0.031s       3.08e-04s    100   723   SoftmaxWithBias(Dot22.0, output_modality_net.b)
	   0.0%    99.0%       0.021s       2.07e-04s    100   733   Elemwise{sqr,no_inplace}(Subtensor{int64:int64:int64}.0)
	   0.0%    99.0%       0.012s       1.17e-04s    100   907   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.0%       0.011s       1.14e-04s    100   491   Alloc(TensorConstant{0.0}, Elemwise{add,no_inplace}.0, TensorConstant{1}, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0)
	   0.0%    99.1%       0.011s       1.12e-04s    100   487   Alloc(TensorConstant{0.0}, Elemwise{add,no_inplace}.0, TensorConstant{1}, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0)
	   0.0%    99.1%       0.011s       1.08e-04s    100   716   Dot22(Reshape{2}.0, output_modality_net.W)
	   0.0%    99.1%       0.010s       9.90e-05s    100   912   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.1%       0.009s       9.39e-05s    100   765   Dot22(SoftmaxGrad.0, output_modality_net.W.T)
	   0.0%    99.1%       0.008s       8.38e-05s    100   918   IncSubtensor{Inc;:int64:}(Alloc.0, Subtensor{::int64}.0, ScalarFromTensor.0)
	   0.0%    99.2%       0.008s       8.29e-05s    100   764   Dot22(InplaceDimShuffle{1,0}.0, SoftmaxGrad.0)
	   0.0%    99.2%       0.007s       7.10e-05s    100   755   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(Alloc.0, Elemwise{Composite{((-i0) / i1)}}.0, Subtensor{int64}.0, Subtensor{int64}.0)
	   0.0%    99.2%       0.007s       6.69e-05s    100   1236   Gemm{inplace}(Alloc.0, TensorConstant{1.0}, Reshape{2}.0, Reshape{2}.0, TensorConstant{1.0})
	   0.0%    99.2%       0.006s       6.18e-05s    100   914   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.2%       0.006s       6.09e-05s    100   916   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.2%       0.006s       5.89e-05s    100    74   Join(TensorConstant{0}, read0.read0.shift.W, read1.read1.shift.W, read2.read2.shift.W, read3.read3.shift.W)
	   0.0%    99.2%       0.005s       5.18e-05s    100   1257   Dot22(InplaceDimShuffle{1,0}.0, Elemwise{Composite{((i0 * i1) + (i0 * i1 * sgn(i2)))}}[(0, 1)].0)
	   0.0%    99.2%       0.005s       5.01e-05s    100   431   Reshape{2}(InplaceDimShuffle{1,0,2}.0, MakeVector{dtype='int64'}.0)
	   0.0%    99.3%       0.005s       4.90e-05s    100   441   AdvancedSubtensor(Reshape{3}.0, Subtensor{int64}.0, Subtensor{int64}.0)
	   ... (remaining 1268 Apply instances account for 0.75%(0.37s) of the runtime)
	
	Here are tips to potentially make your code run faster
	                 (if you think of new ones, suggest them on the mailing list).
	                 Test them first, as they are not guaranteed to always provide a speedup.
	  - Try installing amdlibm and set the Theano flag lib.amdlibm=True. This speeds up only some Elemwise operation.

また、grad_of_scan_fn は以下のようになった。

	:::bash
	Scan Op profiling ( grad_of_scan_fn&grad_of_scan_fn )
	==================
	  Message: None
	  Time in 100 calls of the op (for a total of 8680 steps) 4.361261e+01s
	
	  Total time spent in calling the VM 4.090440e+01s (93.790%)
	  Total overhead (computing slices..) 2.708209e+00s (6.210%)
	
	Class
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Class name>
	  26.9%    26.9%       9.692s       2.86e-06s     C   3393880     391   theano.tensor.elemwise.Elemwise
	  15.3%    42.2%       5.517s       3.97e-05s     Py  138880      16   theano.tensor.basic.Split
	   8.1%    50.3%       2.925s       6.74e-06s     C   434000      50   theano.tensor.blas.Dot22
	   7.5%    57.8%       2.686s       7.74e-05s     C    34720       4   theano.tensor.nnet.corr.CorrMM_gradInputs
	   5.6%    63.4%       2.031s       5.85e-05s     C    34720       4   theano.tensor.nnet.corr.CorrMM_gradWeights
	   3.8%    67.2%       1.371s       2.47e-06s     C   555520      64   theano.tensor.elemwise.Sum
	   3.6%    70.8%       1.293s       3.72e-05s     Py   34720       4   theano.tensor.subtensor.AdvancedIncSubtensor
	   3.3%    74.1%       1.202s       1.08e-06s     C   1111040     128   theano.tensor.elemwise.DimShuffle
	   3.3%    77.4%       1.195s       1.22e-06s     C   980840     113   theano.tensor.basic.Reshape
	   2.7%    80.2%       0.984s       5.67e-05s     C    17360       2   theano.tensor.nnet.corr.CorrMM
	   2.4%    82.6%       0.874s       6.71e-06s     C   130200      15   theano.tensor.blas.BatchedDot
	   1.8%    84.3%       0.631s       9.09e-06s     C    69440       8   theano.tensor.blas_c.CGemv
	   1.7%    86.1%       0.631s       1.04e-06s     C   607600      70   theano.tensor.subtensor.Subtensor
	   1.7%    87.8%       0.625s       3.60e-05s     Py   17360       2   theano.tensor.subtensor.AdvancedSubtensor
	   1.7%    89.5%       0.618s       8.91e-06s     C    69440       8   theano.tensor.blas.Dot22Scalar
	   1.5%    91.0%       0.532s       1.53e-05s     C    34720       4   theano.tensor.subtensor.IncSubtensor
	   1.5%    92.5%       0.532s       1.02e-05s     C    52080       6   theano.tensor.blas.Gemm
	   1.3%    93.8%       0.464s       3.56e-06s     C   130200      15   theano.tensor.basic.Join
	   1.1%    94.9%       0.406s       2.34e-05s     Py   17360       2   theano.tensor.basic.ARange
	   1.0%    95.9%       0.364s       1.05e-05s     C    34720       4   theano.tensor.nnet.nnet.Softmax
	   ... (remaining 10 Classes account for   4.09%(1.48s) of the runtime)
	
	Ops
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Op name>
	   9.1%     9.1%       3.277s       3.78e-05s     Py    86800       10   Split{4}
	   8.1%    17.2%       2.925s       6.74e-06s     C     434000       50   Dot22
	   7.5%    24.7%       2.686s       7.74e-05s     C     34720        4   CorrMM_gradInputs{valid, (1, 1)}
	   6.2%    30.9%       2.240s       4.30e-05s     Py    52080        6   Split{2}
	   5.9%    36.8%       2.125s       2.95e-06s     C     720440       83   Elemwise{mul,no_inplace}
	   5.6%    42.4%       2.031s       5.85e-05s     C     34720        4   CorrMM_gradWeights{valid, (1, 1)}
	   4.9%    47.3%       1.774s       2.49e-06s     C     711760       82   Elemwise{add,no_inplace}
	   3.6%    50.9%       1.293s       3.72e-05s     Py    34720        4   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}
	   2.7%    53.6%       0.984s       5.67e-05s     C     17360        2   CorrMM{valid, (1, 1)}
	   2.4%    56.1%       0.874s       6.71e-06s     C     130200       15   BatchedDot
	   2.0%    58.0%       0.705s       1.14e-06s     C     616280       71   Reshape{2}
	   1.8%    59.8%       0.635s       2.22e-06s     C     286440       33   Sum{axis=[2], acc_dtype=float64}
	   1.7%    61.5%       0.625s       3.60e-05s     Py    17360        2   AdvancedSubtensor
	   1.7%    63.2%       0.618s       8.91e-06s     C     69440        8   Dot22Scalar
	   1.5%    64.7%       0.532s       1.02e-05s     C     52080        6   Gemm{inplace}
	   1.4%    66.1%       0.504s       9.36e-07s     C     538160       62   Subtensor{int64}
	   1.4%    67.5%       0.490s       1.35e-06s     C     364560       42   Reshape{3}
	   1.3%    68.7%       0.464s       3.56e-06s     C     130200       15   Join
	   1.2%    70.0%       0.441s       1.69e-05s     C     26040        3   Elemwise{pow}
	   1.1%    71.1%       0.406s       2.34e-05s     Py    17360        2   ARange{dtype='int64'}
	   ... (remaining 107 Ops account for  28.90%(10.42s) of the runtime)
	
	Apply
		------
	<% time> <sum %> <apply time> <time per call> <#call> <id> <Apply name>
	   2.8%     2.8%       1.027s       1.18e-04s   8680   514   CorrMM_gradInputs{valid, (1, 1)}(Subtensor{::, ::, ::int64, ::int64}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.8%     5.7%       1.019s       1.17e-04s   8680   516   CorrMM_gradInputs{valid, (1, 1)}(Subtensor{::, ::, ::int64, ::int64}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.3%     7.9%       0.819s       9.44e-05s   8680   515   CorrMM_gradWeights{valid, (1, 1)}(Subtensor{::, ::, ::, :int64:}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.3%    10.2%       0.815s       9.39e-05s   8680   517   CorrMM_gradWeights{valid, (1, 1)}(Subtensor{::, ::, ::, :int64:}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.1%    12.3%       0.756s       8.71e-05s   8680   440   CorrMM{valid, (1, 1)}(Subtensor{::, ::, ::, :int64:}.0, Subtensor{::, ::, ::int64, ::int64}.0)
	   2.0%    14.3%       0.726s       8.37e-05s   8680   736   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   1.3%    15.6%       0.473s       5.45e-05s   8680   583   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   1.3%    16.9%       0.457s       5.27e-05s   8680   836   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   1.3%    18.2%       0.451s       5.20e-05s   8680   521   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(1, 1, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   1.2%    19.4%       0.450s       5.19e-05s   8680   966   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
	   1.1%    20.5%       0.406s       4.68e-05s   8680   443   AdvancedSubtensor(CorrMM{valid, (1, 1)}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   1.1%    21.7%       0.406s       4.67e-05s   8680   552   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   1.1%    22.7%       0.395s       4.55e-05s   8680   877   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   1.0%    23.7%       0.352s       4.05e-05s   8680   967   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
	   1.0%    24.7%       0.345s       3.98e-05s   8680   531   CorrMM_gradInputs{valid, (1, 1)}(Subtensor{::, ::, ::int64, ::int64}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   0.9%    25.6%       0.314s       3.62e-05s   8680   663   Dot22(InplaceDimShuffle{1,0}.0, Reshape{2}.0)
	   0.8%    26.4%       0.295s       3.40e-05s   8680   533   CorrMM_gradInputs{valid, (1, 1)}(Subtensor{::, ::, ::int64, ::int64}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   0.8%    27.2%       0.290s       3.34e-05s   8680   506   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(4, 4, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   0.8%    28.0%       0.287s       3.31e-05s   8680   507   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(4, 4, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   0.8%    28.8%       0.281s       3.23e-05s   8680   592   Split{2}(IncSubtensor{InplaceInc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   ... (remaining 1044 Apply instances account for 71.25%(25.68s) of the runtime)
	
	Here are tips to potentially make your code run faster
	                 (if you think of new ones, suggest them on the mailing list).
	                 Test them first, as they are not guaranteed to always provide a speedup.
	  - Try installing amdlibm and set the Theano flag lib.amdlibm=True. This speeds up only some Elemwise operation.

上記の通り、theano.tensor.blas.~ 系が <type> C となっており、Time in 100 calls to Function.__call__ が 5.591766e+01s から 4.939490e+01s になっている。
一応速度を 0.883 倍にできたっぽい。


# Install amdlibm
Profile の結果に散々書かれているように、amdlibm を使うと elemwise 演算の速度向上が期待できるっぽい。

そこで、amdlibm を[ここ](http://developer.amd.com/amd-cpu-libraries/amd-math-library-libm/)からダウンロードし、[ここ](https://hvasbath.github.io/beat/installation.html)を参考にインストールした。

その後の profile 結果は以下の通り。

	:::bash
	Function profiling
	==================
	  Message: examples/run_tasks.py:376
	  Time in 100 calls to Function.__call__: 4.898488e+01s
	  Time in Function.fn.__call__: 4.892176e+01s (99.871%)
	  Time in thunks: 4.854884e+01s (99.110%)
	  Total compile time: 9.918714e+02s
	    Number of Apply nodes: 1288
	    Theano Optimizer time: 9.340450e+02s
	       Theano validate time: 1.014861e+01s
	    Theano Linker time (includes C, CUDA code generation/compiling): 5.377673e+01s
	       Import time 6.545787e-01s
	
	Time in all call to theano.grad() 2.948562e+01s
	Time since theano import 1094.254s
	Class
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Class name>
	  98.6%    98.6%      47.865s       2.39e-01s     Py     200       2   theano.scan_module.scan_op.Scan
	   0.9%    99.5%       0.421s       6.14e-06s     C    68500     685   theano.tensor.elemwise.Elemwise
	   0.2%    99.6%       0.078s       7.83e-05s     C     1000      10   theano.tensor.blas.Dot22
	   0.1%    99.7%       0.055s       7.25e-06s     C     7600      76   theano.tensor.basic.Alloc
	   0.0%    99.8%       0.017s       5.74e-05s     C      300       3   theano.tensor.blas.Gemm
	   0.0%    99.8%       0.013s       7.57e-07s     C    17300     173   theano.compile.ops.Shape_i
	   0.0%    99.8%       0.012s       1.47e-05s     C      800       8   theano.tensor.subtensor.IncSubtensor
	   0.0%    99.8%       0.012s       8.85e-06s     C     1300      13   theano.tensor.basic.Join
	   0.0%    99.9%       0.010s       2.86e-06s     C     3600      36   theano.tensor.basic.Reshape
	   0.0%    99.9%       0.009s       1.17e-06s     C     7500      75   theano.tensor.subtensor.Subtensor
	   0.0%    99.9%       0.008s       4.09e-05s     Py     200       2   theano.tensor.subtensor.AdvancedSubtensor
	   0.0%    99.9%       0.008s       8.03e-05s     C      100       1   theano.tensor.nnet.nnet.SoftmaxWithBias
	   0.0%    99.9%       0.008s       1.07e-06s     C     7100      71   theano.tensor.elemwise.DimShuffle
	   0.0%    99.9%       0.007s       6.79e-05s     Py     100       1   theano.tensor.subtensor.AdvancedIncSubtensor
	   0.0%   100.0%       0.007s       8.55e-07s     C     7700      77   theano.tensor.opt.MakeVector
	   0.0%   100.0%       0.004s       4.45e-05s     Py     100       1   theano.tensor.basic.Nonzero
	   0.0%   100.0%       0.004s       3.84e-05s     C      100       1   theano.tensor.nnet.nnet.SoftmaxGrad
	   0.0%   100.0%       0.003s       7.90e-06s     C      400       4   theano.tensor.elemwise.Sum
	   0.0%   100.0%       0.003s       1.55e-05s     C      200       2   theano.tensor.subtensor.AdvancedSubtensor1
	   0.0%   100.0%       0.001s       1.34e-05s     C      100       1   theano.compile.ops.DeepCopyOp
	   ... (remaining 5 Classes account for   0.01%(0.00s) of the runtime)
	
	Ops
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Op name>
	  89.9%    89.9%      43.644s       4.36e-01s     Py     100        1   forall_inplace,cpu,grad_of_scan_fn&grad_of_scan_fn}
	   8.7%    98.6%       4.222s       4.22e-02s     Py     100        1   forall_inplace,cpu,scan_fn}
	   0.3%    98.9%       0.139s       2.35e-05s     C     5900       59   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)]
	   0.2%    99.0%       0.078s       7.83e-05s     C     1000       10   Dot22
	   0.1%    99.2%       0.055s       7.25e-06s     C     7600       76   Alloc
	   0.1%    99.3%       0.053s       6.62e-05s     C      800        8   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}
	   0.1%    99.3%       0.034s       5.71e-06s     C     6000       60   Elemwise{Clip}[(0, 0)]
	   0.1%    99.4%       0.031s       2.74e-06s     C     11300      113   Elemwise{Add}[(0, 0)]
	   0.1%    99.4%       0.026s       4.34e-06s     C     5900       59   Elemwise{Composite{((i0 * i1) + (i2 * i3))}}
	   0.0%    99.5%       0.022s       3.07e-06s     C     7000       70   Elemwise{Composite{(i0 * sqr(i1))}}
	   0.0%    99.5%       0.021s       2.95e-06s     C     7000       70   Elemwise{Mul}[(0, 1)]
	   0.0%    99.6%       0.020s       2.01e-04s     C      100        1   Elemwise{sqr,no_inplace}
	   0.0%    99.6%       0.020s       3.18e-06s     C     6200       62   Elemwise{add,no_inplace}
	   0.0%    99.7%       0.017s       5.74e-05s     C      300        3   Gemm{inplace}
	   0.0%    99.7%       0.013s       6.44e-05s     C      200        2   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 3)]
	   0.0%    99.7%       0.012s       8.85e-06s     C     1300       13   Join
	   0.0%    99.7%       0.009s       3.45e-06s     C     2700       27   Reshape{2}
	   0.0%    99.7%       0.009s       8.57e-05s     C      100        1   IncSubtensor{Inc;:int64:}
	   0.0%    99.8%       0.008s       4.09e-05s     Py     200        2   AdvancedSubtensor
	   0.0%    99.8%       0.008s       7.36e-06s     C     1100       11   Elemwise{clip,no_inplace}
	   ... (remaining 109 Ops account for   0.23%(0.11s) of the runtime)
	
	Apply
	------
	<% time> <sum %> <apply time> <time per call> <#call> <id> <Apply name>
	  89.9%    89.9%      43.644s       4.36e-01s    100   783   forall_inplace,cpu,grad_of_scan_fn&grad_of_scan_fn}(Elemwise{Composite{Switch(EQ(i0, i1), ((i2 * i3) // (i4 * i0)), i0)}}.0, Elemwise{sqr,no_inplace}.0, InplaceDimShuffle{0,1,3,2}.0, InplaceDimShuffle{0,1,3,2}.0, InplaceDimShuffle{0,1,2}.0, InplaceDimShuffle{0,1,2,3,x}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int64:int64}.0, Subtensor{int64:int6
	   8.7%    98.6%       4.222s       4.22e-02s    100   688   forall_inplace,cpu,scan_fn}(Elemwise{Composite{Switch(EQ(i0, i1), ((i2 * i3) // (i4 * i0)), i0)}}.0, Subtensor{int64:int64:int8}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, IncSubtensor{InplaceSet;:int64:}.0, controller.W_in_and_reads_to_o01, controller.W_hid_to_o01, controller.W_in_and_reads_to_i01, controller.W_hid_to_i01, controller.W_in_and_rea
	   0.0%    98.6%       0.020s       2.01e-04s    100   733   Elemwise{sqr,no_inplace}(Subtensor{int64:int64:int64}.0)
	   0.0%    98.7%       0.019s       1.93e-04s    100   776   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}(TensorConstant{(1, 1) of 0.9}, <TensorType(float32, matrix)>, TensorConstant{(1, 1) of 0.0001}, Elemwise{clip,no_inplace}.0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}[(0, 1)].0)
	   0.0%    98.7%       0.016s       1.58e-04s    100   1234   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}(TensorConstant{(1, 1) of 0.9}, <TensorType(float32, matrix)>, TensorConstant{(1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    98.7%       0.016s       1.58e-04s    100   1048   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}(TensorConstant{(1, 1, 1) of 0.9}, <TensorType(float32, 3D)>, TensorConstant{(1, 1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}[(0, 1)].0)
	   0.0%    98.8%       0.013s       1.28e-04s    100   1069   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1, 1) of 0.9}, <TensorType(float32, 3D)>, TensorConstant{(1, 1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    98.8%       0.013s       1.27e-04s    100   1059   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1, 1) of 0.9}, <TensorType(float32, 3D)>, TensorConstant{(1, 1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    98.8%       0.013s       1.27e-04s    100   1079   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1, 1) of 0.9}, <TensorType(float32, 3D)>, TensorConstant{(1, 1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}[(0, 1)].0)
	   0.0%    98.8%       0.013s       1.27e-04s    100   1240   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 3)](TensorConstant{(1, 1) of 0.9}, <TensorType(float32, matrix)>, TensorConstant{(1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    98.9%       0.013s       1.26e-04s    100   1093   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1, 1) of 0.9}, <TensorType(float32, 3D)>, TensorConstant{(1, 1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    98.9%       0.013s       1.26e-04s    100   1241   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1) of 0.9}, <TensorType(float32, matrix)>, TensorConstant{(1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    98.9%       0.013s       1.26e-04s    100   1242   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1) of 0.9}, <TensorType(float32, matrix)>, TensorConstant{(1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    98.9%       0.012s       1.21e-04s    100   907   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.0%       0.011s       1.12e-04s    100   716   Dot22(Reshape{2}.0, output_modality_net.W)
	   0.0%    99.0%       0.011s       1.11e-04s    100   487   Alloc(TensorConstant{0.0}, Elemwise{add,no_inplace}.0, TensorConstant{1}, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0)
	   0.0%    99.0%       0.011s       1.10e-04s    100   491   Alloc(TensorConstant{0.0}, Elemwise{add,no_inplace}.0, TensorConstant{1}, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0, Elemwise{Composite{Switch(EQ(i0, i1), i2, i0)}}.0)
	   0.0%    99.0%       0.011s       1.10e-04s    100   912   Dot22(Reshape{2}.0, Reshape{2}.0)
	   0.0%    99.1%       0.010s       9.90e-05s    100   1269   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1) of 0.9}, <TensorType(float32, matrix)>, TensorConstant{(1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   0.0%    99.1%       0.010s       9.89e-05s    100   1270   Elemwise{Composite{((i0 * i1) - ((i2 * i3) / sqrt((i2 + i4 + i5 + sqr(i6)))))}}[(0, 1)](TensorConstant{(1, 1) of 0.9}, <TensorType(float32, matrix)>, TensorConstant{(1, 1) of 0.0001}, Elemwise{Clip}[(0, 0)].0, Elemwise{Mul}[(0, 1)].0, Elemwise{Composite{(i0 * sqr(i1))}}.0, Elemwise{Composite{((i0 * i1) + (i2 * i3))}}.0)
	   ... (remaining 1268 Apply instances account for 0.92%(0.45s) of the runtime)
	
	Here are tips to potentially make your code run faster
	                 (if you think of new ones, suggest them on the mailing list).
	                 Test them first, as they are not guaranteed to always provide a speedup.
	  Sorry, no tip for today.

また、grad_of_scan_fn は以下の通り。

	:::bash
	Scan Op profiling ( grad_of_scan_fn&grad_of_scan_fn )
	==================
	  Message: None
	  Time in 100 calls of the op (for a total of 8700 steps) 4.326865e+01s
	
	  Total time spent in calling the VM 4.045974e+01s (93.508%)
	  Total overhead (computing slices..) 2.808916e+00s (6.492%)
	
	Class
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Class name>
	  25.5%    25.5%       9.022s       2.65e-06s     C   3401700     391   theano.tensor.elemwise.Elemwise
	  16.3%    41.7%       5.757s       4.14e-05s     Py  139200      16   theano.tensor.basic.Split
	   8.4%    50.1%       2.958s       6.80e-06s     C   435000      50   theano.tensor.blas.Dot22
	   7.4%    57.5%       2.615s       7.52e-05s     C    34800       4   theano.tensor.nnet.corr.CorrMM_gradInputs
	   5.7%    63.1%       2.007s       5.77e-05s     C    34800       4   theano.tensor.nnet.corr.CorrMM_gradWeights
	   4.0%    67.1%       1.401s       2.52e-06s     C   556800      64   theano.tensor.elemwise.Sum
	   3.7%    70.8%       1.312s       3.77e-05s     Py   34800       4   theano.tensor.subtensor.AdvancedIncSubtensor
	   3.6%    74.4%       1.264s       1.13e-06s     C   1113600     128   theano.tensor.elemwise.DimShuffle
	   3.5%    77.9%       1.235s       1.26e-06s     C   983100     113   theano.tensor.basic.Reshape
	   2.8%    80.6%       0.984s       5.65e-05s     C    17400       2   theano.tensor.nnet.corr.CorrMM
	   2.3%    82.9%       0.820s       6.28e-06s     C   130500      15   theano.tensor.blas.BatchedDot
	   1.8%    84.8%       0.650s       9.33e-06s     C    69600       8   theano.tensor.blas.Dot22Scalar
	   1.8%    86.6%       0.644s       1.06e-06s     C   609000      70   theano.tensor.subtensor.Subtensor
	   1.7%    88.4%       0.620s       3.56e-05s     Py   17400       2   theano.tensor.subtensor.AdvancedSubtensor
	   1.7%    90.0%       0.600s       8.63e-06s     C    69600       8   theano.tensor.blas_c.CGemv
	   1.5%    91.5%       0.531s       1.02e-05s     C    52200       6   theano.tensor.blas.Gemm
	   1.3%    92.9%       0.477s       3.66e-06s     C   130500      15   theano.tensor.basic.Join
	   1.3%    94.2%       0.464s       1.33e-05s     C    34800       4   theano.tensor.subtensor.IncSubtensor
	   1.1%    95.3%       0.383s       2.20e-05s     Py   17400       2   theano.tensor.basic.ARange
	   1.0%    96.2%       0.342s       9.36e-07s     C   365400      42   theano.compile.ops.Shape_i
	   ... (remaining 10 Classes account for   3.75%(1.33s) of the runtime)
	
	Ops
	---
	<% time> <sum %> <apply time> <time per call> <type> <#call> <#apply> <Op name>
	   9.6%     9.6%       3.413s       3.92e-05s     Py    87000       10   Split{4}
	   8.4%    18.0%       2.958s       6.80e-06s     C     435000       50   Dot22
	   7.4%    25.4%       2.615s       7.52e-05s     C     34800        4   CorrMM_gradInputs{valid, (1, 1)}
	   6.6%    32.0%       2.344s       4.49e-05s     Py    52200        6   Split{2}
	   5.8%    37.7%       2.038s       2.82e-06s     C     722100       83   Elemwise{mul,no_inplace}
	   5.7%    43.4%       2.007s       5.77e-05s     C     34800        4   CorrMM_gradWeights{valid, (1, 1)}
	   4.9%    48.3%       1.736s       2.43e-06s     C     713400       82   Elemwise{add,no_inplace}
	   3.7%    52.0%       1.312s       3.77e-05s     Py    34800        4   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}
	   2.8%    54.8%       0.984s       5.65e-05s     C     17400        2   CorrMM{valid, (1, 1)}
	   2.3%    57.1%       0.820s       6.28e-06s     C     130500       15   BatchedDot
	   2.1%    59.2%       0.726s       1.18e-06s     C     617700       71   Reshape{2}
	   1.8%    61.0%       0.650s       9.33e-06s     C     69600        8   Dot22Scalar
	   1.8%    62.8%       0.644s       2.24e-06s     C     287100       33   Sum{axis=[2], acc_dtype=float64}
	   1.7%    64.6%       0.620s       3.56e-05s     Py    17400        2   AdvancedSubtensor
	   1.5%    66.1%       0.531s       1.02e-05s     C     52200        6   Gemm{inplace}
	   1.5%    67.5%       0.516s       9.56e-07s     C     539400       62   Subtensor{int64}
	   1.4%    69.0%       0.509s       1.39e-06s     C     365400       42   Reshape{3}
	   1.3%    70.3%       0.477s       3.66e-06s     C     130500       15   Join
	   1.1%    71.4%       0.391s       2.25e-06s     C     174000       20   Sum{axis=[0], acc_dtype=float64}
	   1.1%    72.5%       0.383s       2.20e-05s     Py    17400        2   ARange{dtype='int64'}
	   ... (remaining 107 Ops account for  27.51%(9.74s) of the runtime)
	
	Apply
	------
	<% time> <sum %> <apply time> <time per call> <#call> <id> <Apply name>
	   2.8%     2.8%       0.993s       1.14e-04s   8700   516   CorrMM_gradInputs{valid, (1, 1)}(Subtensor{::, ::, ::int64, ::int64}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.8%     5.6%       0.993s       1.14e-04s   8700   514   CorrMM_gradInputs{valid, (1, 1)}(Subtensor{::, ::, ::int64, ::int64}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.3%     7.9%       0.813s       9.34e-05s   8700   515   CorrMM_gradWeights{valid, (1, 1)}(Subtensor{::, ::, ::, :int64:}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.3%    10.2%       0.807s       9.28e-05s   8700   517   CorrMM_gradWeights{valid, (1, 1)}(Subtensor{::, ::, ::, :int64:}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   2.1%    12.3%       0.758s       8.71e-05s   8700   440   CorrMM{valid, (1, 1)}(Subtensor{::, ::, ::, :int64:}.0, Subtensor{::, ::, ::int64, ::int64}.0)
	   2.1%    14.4%       0.742s       8.53e-05s   8700   736   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   1.4%    15.8%       0.485s       5.57e-05s   8700   966   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
	   1.3%    17.1%       0.476s       5.47e-05s   8700   583   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   1.3%    18.5%       0.475s       5.46e-05s   8700   836   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   1.2%    19.7%       0.433s       4.98e-05s   8700   521   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(1, 1, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   1.2%    20.9%       0.418s       4.81e-05s   8700   552   Split{2}(IncSubtensor{Inc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   1.2%    22.0%       0.415s       4.77e-05s   8700   877   Split{4}(InplaceDimShuffle{1,0,2}.0, TensorConstant{0}, <TensorType(int64, vector)>)
	   1.1%    23.2%       0.397s       4.56e-05s   8700   443   AdvancedSubtensor(CorrMM{valid, (1, 1)}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   1.1%    24.2%       0.377s       4.33e-05s   8700   967   Split{2}(Elemwise{add,no_inplace}.0, TensorConstant{1}, MakeVector{dtype='int64'}.0)
	   1.0%    25.2%       0.342s       3.93e-05s   8700   531   CorrMM_gradInputs{valid, (1, 1)}(Subtensor{::, ::, ::int64, ::int64}.0, AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}.0)
	   0.9%    26.1%       0.316s       3.63e-05s   8700   663   Dot22(InplaceDimShuffle{1,0}.0, Reshape{2}.0)
	   0.9%    27.0%       0.304s       3.50e-05s   8700   506   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(4, 4, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   0.8%    27.8%       0.298s       3.42e-05s   8700   592   Split{2}(IncSubtensor{InplaceInc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   0.8%    28.6%       0.290s       3.34e-05s   8700   507   AdvancedIncSubtensor{inplace=False,  set_instead_of_inc=False}(TensorConstant{(4, 4, 1, ..28) of 0.0}, Reshape{2}.0, ARange{dtype='int64'}.0, ARange{dtype='int64'}.0, TensorConstant{0}, SliceConstant{None, None, None})
	   0.8%    29.4%       0.290s       3.33e-05s   8700   556   Split{2}(IncSubtensor{InplaceInc;::, ::, ::, :int64:}.0, TensorConstant{3}, TensorConstant{(2,) of 128})
	   ... (remaining 1044 Apply instances account for 70.57%(24.99s) of the runtime)
	
	Here are tips to potentially make your code run faster
	                 (if you think of new ones, suggest them on the mailing list).
	                 Test them first, as they are not guaranteed to always provide a speedup.
	  Sorry, no tip for today.

結果確かに elemwise の演算は早くなっており、最終的に Time in 100 calls to Function.__call__ を 4.898488e+01s (最初の 0.876 倍) にできた。
