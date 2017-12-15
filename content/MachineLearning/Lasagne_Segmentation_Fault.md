Title: Lasagne Segmentation Fault
Tags: Programming, Theano, Lasagne,
Date: 2017-10-16 19:00
Modified: 2017-10-16 19:00
Slug: Lasagne_Segmentation_Fault
Authors: guchio3
Summary: Lasagne を GPU 上で使用した際に出る Segmentation Fault への対策

# Outline
Theano 上で動く Deep Learning Library である [Lasagne](https://lasagne.readthedocs.io/en/latest/) を使った[コード](https://github.com/snipsco/ntm-lasagne) GPU 上で使用した際、以下のエラーが出たのでその対策をした。  
このエラーは非常に厄介で、最初は自分で書いた別のプログラムで GPU を使用して際に起こったが、その時はエラーメッセージなしで勝手にプログラムが止まったので原因究明が非常に大変だった。

	:::bash
	$ PYTHONPATH=. python examples/copy-task.py 
	Using cuDNN version 5110 on context None
	Mapped name None to device cuda0: Tesla K80 (0000:83:00.0)
	Segmentation fault (core dumped)

まずは[ここ](https://github.com/Theano/Theano/issues/6141)を参考に、conda を使った際にインストールされる pygpu の version が悪いことを疑って以下を試した。

    $ conda install pygpu=0.6.2

しかし結果は変わらず対策を探していると、[ここ](https://github.com/Theano/Theano/issues/4760)に ~/.theanorc の device を gpu から cuda するとセグフォると書いてあったので device を cuda から gpu にしてみた。  
結果うまく行ったが、gpu にした場合バグが多く効率が悪くまた cuda で使える float64 が使えないとの情報もあるのでよりいい方法があれば追記予定。
