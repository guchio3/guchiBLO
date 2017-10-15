Title: Libgpuarray For Theano 0.8.2
Tags: Theano, Lasagne, Machine Learning,
Date: 2017-10-15 0:00
Modified: 2017-10-15 0:00
Slug: Libgpuarray_For_Theano_0.8.2
Authors: guchio3
Summary: Theano 0.8.2 に適合する libgpuarray のインストール

Theano (ver 0.8.2) から gpu を使用する際、以下のようなエラーが出たので対応した際のログ。

    :::bash
	ERROR (theano.sandbox.gpuarray): Could not initialize pygpu, support disabled
	Traceback (most recent call last):
	  File "/home/guchio/miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/theano/sandbox/gpuarray/__init__.py", line 95, in <module>
	    init_dev(config.device)
	  File "/home/guchio/miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/theano/sandbox/gpuarray/__init__.py", line 46, in init_dev
	    "Make sure Theano and libgpuarray/pygpu "
	RuntimeError: ('Wrong major API version for gpuarray:', 1, 'Make sure Theano and libgpuarray/pygpu are in sync.')

これは [Theano の issue](https://github.com/Theano/libgpuarray/issues/183) を参照するに libgpuarray のバージョンと Theano のバージョンのミスマッチが原因ぽく、libgpuarray の tag v-9998 をインストールすることで解決できるぽい。

そこで[ここ](https://coderwall.com/p/-wbo5q/pip-install-a-specific-github-repo-tag-or-branch)を参考に pip 経由で以下のように libgpuarray をインストールしたが、以下のエラーを確認。  
ちなみに、#egg 以降は[ここ](https://stackoverflow.com/questions/21638929/how-to-determine-the-name-of-an-egg-for-a-python-package-on-github)を参考に、libgpuarray の setup.py を参照した。

    :::bash
    $ pip install -e git://github.com/Theano/libgpuarray.git@v-9998#egg=pygpu
	Obtaining pygpu from git+git://github.com/Theano/libgpuarray.git@v-9998#egg=pygpu
	  Cloning git://github.com/Theano/libgpuarray.git (to v-9998) to ./src/pygpu
	    Complete output from command python setup.py egg_info:
	    Traceback (most recent call last):
	      File "<string>", line 1, in <module>
	      File "/home/guchio/src/pygpu/setup.py", line 7, in <module>
	        import Cython
	    ImportError: No module named Cython
	    
	    ----------------------------------------
	Command "python setup.py egg_info" failed with error code 1 in /home/guchio/src/pygpu/

そこで cython をインストールして再度挑戦。  
しかし以下のエラーを確認。

    :::bash
	$ pip install -e git://github.com/Theano/libgpuarray.git@v-9998#egg=pygpu
	Obtaining pygpu from git+git://github.com/Theano/libgpuarray.git@v-9998#egg=pygpu
	  Updating ./src/pygpu clone (to v-9998)
	Requirement already satisfied: mako>=0.7 in ./miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/Mako-1.0.7-py2.7.egg (from pygpu)
	Requirement already satisfied: MarkupSafe>=0.9.2 in ./miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages (from mako>=0.7->pygpu)
	Installing collected packages: pygpu
	  Found existing installation: pygpu 0.6.9
	    Uninstalling pygpu-0.6.9:
	      Successfully uninstalled pygpu-0.6.9
	  Running setup.py develop for pygpu
    Complete output from command /home/guchio/miniconda2/envs/ntmenv-owl/bin/python -c "import setuptools, tokenize;__file__='/home/guchio/src/pygpu/setup.py';f=getattr(tokenize, 'o
	pen', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" develop --no-deps:
	    running develop
	    running egg_info
	    writing requirements to pygpu.egg-info/requires.txt
	    writing pygpu.egg-info/PKG-INFO
	    writing top-level names to pygpu.egg-info/top_level.txt
	    writing dependency_links to pygpu.egg-info/dependency_links.txt
	    reading manifest file 'pygpu.egg-info/SOURCES.txt'
	    writing manifest file 'pygpu.egg-info/SOURCES.txt'
	    running build_ext
	    building 'pygpu.gpuarray' extension
	    gcc -pthread -B /home/guchio/miniconda2/envs/ntmenv-owl/compiler_compat -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -I/usr/local/cuda/include/ -fPIC -DGPUARRAY_SHARED -I/h
	ome/guchio/miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/numpy/core/include -I/home/guchio/miniconda2/envs/ntmenv-owl/include/python2.7 -c pygpu/gpuarray.c -o build/temp.li
	nux-x86_64-2.7/pygpu/gpuarray.o
	    In file included from /home/guchio/miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/numpy/core/include/numpy/ndarraytypes.h:1809:0,
	                     from /home/guchio/miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/numpy/core/include/numpy/ndarrayobject.h:18,
	                     from /home/guchio/miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/numpy/core/include/numpy/arrayobject.h:4,
	                     from pygpu/gpuarray.c:514:
    /home/guchio/miniconda2/envs/ntmenv-owl/lib/python2.7/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:15:2: warning: #warning "Using deprecated NumPy API, disabl
	e it by " "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
	     #warning "Using deprecated NumPy API, disable it by " \
	      ^
	    pygpu/gpuarray.c:516:28: fatal error: gpuarray/types.h: No such file or directory
	    compilation terminated.
	    error: command 'gcc' failed with exit status 1
	    
	    ----------------------------------------
	  Rolling back uninstall of pygpu
	Command "/home/guchio/miniconda2/envs/ntmenv-owl/bin/python -c "import setuptools, tokenize;__file__='/home/guchio/src/pygpu/setup.py';f=getattr(tokenize, 'open', open)(__file__);co
	de=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" develop --no-deps" failed with error code 1 in /home/guchio/src/pygpu/

その後いろいろ試したがうまく行かず、結局 Theano のバージョンを 0.8.2 から 0.9.0 に変更して解決した。  
試しに gpu の速度を次のコードで図った。

	:::python
	from theano import function, config, shared, tensor
	import numpy
	import time
	
	vlen = 10 * 30 * 768  # 10 x #cores x # threads per core
	iters = 1000
	
	rng = numpy.random.RandomState(22)
	x = shared(numpy.asarray(rng.rand(vlen), config.floatX))
	f = function([], tensor.exp(x))
	print(f.maker.fgraph.toposort())
	t0 = time.time()
	for i in range(iters):
	    r = f()
	t1 = time.time()
	print("Looping %d times took %f seconds" % (iters, t1 - t0))
	print("Result is %s" % (r,))
	if numpy.any([isinstance(x.op, tensor.Elemwise) and
	              ('Gpu' not in type(x.op).__name__)
	              for x in f.maker.fgraph.toposort()]):
	    print('Used the cpu')
	else:
	    print('Used the gpu')

結果は以下。(cpu は 1 core のみ使用。)

	:::bash
	# GPU ver
	Using cuDNN version 5110 on context None
	Mapped name None to device cuda0: Tesla K80 (0000:83:00.0)
	[GpuElemwise{exp,no_inplace}(<GpuArrayType<None>(float32, (False,))>), HostFromGpu(gpuarray)(GpuElemwise{exp,no_inplace}.0)]
	Looping 1000 times took 0.505921 seconds
	Result is [ 1.23178029  1.61879349  1.52278066 ...,  2.20771813  2.29967761  1.62323296]
	Used the gpu

	# CPU ver
	[Elemwise{exp,no_inplace}(<TensorType(float32, vector)>)]
	Looping 1000 times took 32.001292 seconds
	Result is [ 1.23178029  1.61879337  1.52278066 ...,  2.20771813  2.29967761  1.62323284]
	Used the cpu

一方、[以前の記事](https://guchio3.github.io/guchiBLO/Speeding_Up_Theano.html)で紹介した amdlibm を使用すると cpu でも以下のように良い結果となった。  
今回の elementwise は amdlibm の効果が非常に出やすいものっぽい。

	:::bash
	# CPU w/ amdlibm ver
	[Elemwise{exp,no_inplace}(<TensorType(float32, vector)>)]
	Looping 1000 times took 1.445175 seconds
	Result is [ 1.23178029  1.61879337  1.52278066 ...,  2.20771813  2.29967761  1.62323284]
	Used the cpu

また、Theano 0.9.0 は今使っている Lasagne というライブラリの 0.1 との相性が悪く、lasagne/layers/pool.py に於いて

	:::python
	from theano.tensor.signal import downsample 

という行があるが、theano 0.9.0 は downsample をサポートから外しているため、ここで下のようなエラーが出る。

	:::bash
	ImportError: cannot import name downsample

一方 Lasagne 全体を bleeeding edge version にしてしまうと今書いているプログラムが動かなくなるため、あまり良い手ではないがこの pool.py だけ[最新のもの](https://github.com/Lasagne/Lasagne/blob/master/lasagne/layers/pool.py)に手で書き換え解決。
