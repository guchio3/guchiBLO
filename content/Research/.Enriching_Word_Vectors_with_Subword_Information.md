Title: Enriching Word Vectors with Subword Information
Tags: Papers, Machine Learning, Distributed Representation, 
Date: 2017-09-24 10:00
Modified: 2017-09-24 10:00
Slug: Enriching_Word_Vectors_with_Subword_Information
Authors: guchio3
Summary: 構成文字を考慮した新しい単語の分散表現生成手法

# Outline
単語を分散表現する場合、Word2vec などは単語を最小単位として扱った学習によりこれを実現するが、この論文の提案手法では Subword (部分語) に基づいてこれを行う。

具体的には各単語をその単語中の character n-grams の集合により表現し (一方 Word2vec では word n-grams を使用しており、何を基準とした n-gram かは意識する必要あり)、各 subword に対応するベクトルの和によって単語全体を表すベクトルを表す。 

これには次のようなメリットがある。 

* Prefix や Suffix といった形態素情報を加味した分散表現が可能
* 未知語に対応
* 学習が高速... (なぜ高速か、どういう意味で高速かは理解できていない)


___
# Contents
提案手法は非常にシンプル (これもこの手法の良い点の一つ)。以下にその詳細を示す。

### Skip-gram
この論文の提案手法による学習は Skip-gram ([Mikilov et al., 2013](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf)) ベースで行われる。

Skip-gram は、**単語はその文章中での使われ方、つまりその前後にどのような単語が出現するかによりその意味が定義される**というアイデアに基づいて単語の分散表現を学習する手法である。Skip-gram については[~さんのブログ](https://google.com)でわかりやすい説明をして下さっている。

例えば apple, egg そして umbrella という３つの単語について考える。apple と egg は食べ物という意味である程度親しい意味を持っており、これらはどちらも "I ate an * for breakfast." の (* は apple または egg) という使われ方をされうる。一方、"I ate an umbrella for breakfast" という使われ方は普通されない。すなわち例の様に、似ている意味を持つ単語ほど似ている使い方をされやすい、つまり前後に似た単語が現れやすい。(この例はあまり良くなさそう...)

このアイデアに基づき Skip-gram では文章、つまり単語系列 $w_1, w_2, ..., w_n$ 中のある単語 $w_t$ の分散表現を学習する際、$w_t$ のベクトル表現が以下の式を満たすように学習が行われる。
$$ \sin{a} $$
ここで、~。

しかし Skip-gram は単語を最小単位とした学習を行うため、次の２つの問題を抱える。

* Prefix や Suffix といった形態素情報を加味できない
* 未知語に非対応

この論文で提案する手法では学習時に扱う最小単位を単語から subword へと変更することでこれらの問題に対処できる。

### Proposal
提案手法では各単語をその subword、具体的には character n-grams により表現することを試みる (この論文では 3 ~ 6-gram を使用)。

例えば、"where" という単語の character 3-grams は 
$$ '<wh', 'whe', 'her', 'ere', 're>' $$
の５つである。ここで、$<$ および $>$ は単語の最初および最後を表す文字を示す。

あとは各 n-gram の分散表現を Skip-gram と同様の学習アルゴリズムにより獲得し、以下のように単語の分散表現を獲得する。
$$ sin{a} $$
ここで、~。

上記の内容から、この提案手法が Prefix や Suffix といった形態素情報を加味した分散表現が可能であり、また各 n-gram の分散表現学習さえ行えてしまえば未知語への対応も可能なことがわかる。


___
# Discussion
また面白いネタを見つけ次第随時更新していきます！


___
# References
[Original Paper](https://pdfs.semanticscholar.org/e2db/a792360873aef125572812f3673b1a85d850.pdf)
