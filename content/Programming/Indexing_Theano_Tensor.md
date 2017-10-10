Title: Indexing Theano Tensor
Tags: Theano, Machine Learning,
Date: 2017-10-08 0:00
Modified: 2017-10-08 0:00
Slug: Indexing_Theano_Tensor
Authors: guchio3
Summary: Theano tensor を条件に基いて indexing する方法

# Outline
Thenao tensor の要素のうち条件を満たすものを抽出する方法。  
私の場合は [bAbI task](https://research.fb.com/downloads/babi/) という質問応答処理タスクを DL を使用して解く実装を行う際、 word の系列からモデルの応答に当たるものだけを抽出するのに用いたのでメモ。

様々な実装があると思うが、今回は以下に示す方法により行った。  
具体的には、theano.tensor.eq と .nonzero() を用いて抽出したい箇所のインデックスを示すマスクを生成し、これにより抽出を行う。

---
# Details
次のような同じ系列長の２つの vector $v_a$, $v_b$ があるとき、$v_a$ の要素が 0 となっている箇所に対応する $v_b$ の要素のみを抽出したい。

    :::python
    v_a = [2, 1, 4, 5, 0, 10, 8, 7, 0, 11, 2, 3, 0]
    v_b = [2, 3, 1, 9, 9, 12, 1, 1, 7, 10, 2, 4, 1]

以下が Theano 実装の一例。

    :::python
    import theano
    import theano.tensor as T
    
    v_a = T.vector('v_a')
    v_b = T.vector('v_b')
    ans_mask = T.eq(v_a, 0).nonzero()
    
    answers = v_b[ans_mask]
    fn = theano.function([v_a, v_b], answers)
    
    example_v_a = [2, 1, 4, 5, 0, 10, 8, 7, 0, 11, 2, 3, 0]
    example_v_b = [2, 3, 1, 9, 9, 12, 1, 1, 7, 10, 2, 4, 1]
    
    print(fn(example_v_a, example_v_b))
    # [ 9.  7.  1.]

ちなみに、T.eq を適用後および .nonzero() を適用後のベクトルは以下のようになっている。

    :::python
    import theano
    import theano.tensor as T

    v_a = T.vector('v_a')

    eq_ans_mask = T.eq(v_a, 0)
    nonzero_ans_mask = T.eq(v_a, 0).nonzero()
    eq_fn = theano.function([v_a], eq_ans_mask)
    nonzero_fn = theano.function([v_a], nonzero_ans_mask)

    example_v_a = [2, 1, 4, 5, 0, 10, 8, 7, 0, 11, 2, 3, 0]

    print(eq_fn(example_v_a))
    # [0 0 0 0 1 0 0 0 1 0 0 0 1]
    print(nonzero_fn(example_v_a))
    # [array([ 4,  8, 12])] ])]
