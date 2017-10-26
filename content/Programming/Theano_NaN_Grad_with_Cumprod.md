Title: Theano NaN Grad with Cumprod
Tags: Theano, Machine Learning,
Date: 2017-10-26 0:00
Modified: 2017-10-26 0:00
Slug: Theano_NaN_Grad_with_Cumprod
Authors: guchio3
Summary: Theano の cumprod を利用する際に gradient が NaN になるバグ

以前 [Differentiable neural computers](https://www.nature.com/nature/journal/v538/n7626/full/nature20101.html) を実装した際、

\begin{equation}
\label{a_t_equation}
    {\bf a}_t[\phi_t[j]] = (1 - {\bf u}_t[\phi_t[j]])\prod_{i=1}^{j-1}{\bf u}_t[\phi_t[i]])
\end{equation}

という式を Theano で実装するため theano.tensor.extra_ops.cumprod を使用した際に遭遇したバグ共有。

症状としては gradient を計算をすると 1 iteration 目から NaN が現れるというものだったが [ここ](https://github.com/Theano/Theano/issues/5197)をみて解決。  
どうやら入力に 0 が入ると　gradien 計算において  0 割りがおこり、NaN が出現するらしい。

結果として行ったことは justheuristic さんが書いてくれているコードをそのまま使っただけだが、問題は解決した。
