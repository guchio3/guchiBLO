Title: Back Propagation For RNN
Tags: Recurrent Neural Network, Machine Learning,
Date: 2017-11-26 0:00
Modified: 2017-11-27 0:00
Slug: Back-Propagation-For-RNN
Authors: guchio3
Summary: RNN における Back Probagation 

# Outline

以下の様に Forward 方向の式が表される単純な Recurrent Neural Network (RNN) における誤差伝搬を数式をたどることにより理解する。  
行列の計算は [matrix cookbook](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf) が非常に参考になった。  
なお、バイアスは簡単のため無視し、また以下で偏微分でない分数形式の記述は要素毎の割り算を意味。

\begin{equation}
    \begin{split}
        \bar{\bf h}_t &= W_i{\bf x_t} + W_h{\bf h_{t-1}} \\
        {\bf h}_t &= f_1(\bar{\bf h}_t) \\
        \bar{\bf y}_t &= W_o \cdot {\bf h}_t \\
        {\bf y}_t &= f_2(\bar{\bf y}_t)
    \end{split}
\end{equation}
なお、以下のように活性化関数 $f_2$ には softmax 関数を用い、誤差関数にはクロスエントロピー関数を使用。
\begin{equation}
    f_2({\bf v}_i) = \frac{exp({\bf v}_i)}{\sum_j exp({\bf v}_j)}
\end{equation}
\begin{equation}
\label{cross_entropy}
    E = - \sum_{t'}{\bf l}_{t'}^T \cdot log({\bf y}_{t'})
\end{equation}
なお、${\bf v}_i$ は ${\bf v}$ の $i$ 番目の要素を表し、${\bf l}_t$ は時間 $t$ における正解ラベルを表す。

このとき、Back Probagation により $W_o, W_i, W_h$ を学習することを考える。  
これは誤差関数 $E$ を各パラメータにより次のように偏微分することにより求められる。
\begin{equation}
\label{target_round}
    \begin{split}
        \frac{\partial E}{\partial W_{o}} &= \frac{\partial \bar{\bf y}_t}{\partial W_{o}} \cdot \frac{\partial E}{\partial \bar{\bf y}_t} = {\bf h}_t \cdot \frac{\partial E}{\partial \bar{\bf y}_t} \\
        \frac{\partial E}{\partial W_{i}} &= \frac{\partial \bar{\bf h}_t}{\partial W_{i}} \cdot \frac{\partial E}{\partial \bar{\bf h}_t} = {\bf x}_t \cdot \frac{\partial E}{\partial \bar{\bf h}_t} \\
        \frac{\partial E}{\partial W_{h}} &= \frac{\partial \bar{\bf h}_t}{\partial W_{h}} \cdot \frac{\partial E}{\partial \bar{\bf h}_t} = {\bf h}_{t-1} \cdot \frac{\partial E}{\partial \bar{\bf h}_t} 
    \end{split}
\end{equation}

よって式 (\ref{target_round}) より、$\frac{\partial E}{\partial \bar{\bf y}_t}$ および $\frac{\partial E}{\partial \bar{\bf h}_t}$ を求めれば良いことになる。

$\frac{\partial E}{\partial \bar{\bf y}_t}$ は以下のように求められる。

\begin{equation}
    \begin{split}
        \frac{\partial E}{\partial \bar{\bf y}_t} &= - \frac{\partial {\bf y}_t}{\partial \bar{\bf y}_t} \cdot \frac{\partial E}{\partial {\bf y}_t} \\
                                                  &= - \frac{\partial {\bf y}_t}{\partial \bar{\bf y}_t} \cdot \sum_{t'}\frac{\partial {\bf y}_{t'}}{\partial {\bf y}_t} \cdot \frac{{\bf l}_{t'}}{{\bf y}_{t'}}
    \end{split}
\end{equation}

$\frac{\partial E}{\partial {\bf y}_t}$ の計算は要素毎に考えてみると分かりやすい。

ここで、$\frac{\partial {\bf y}_t}{\partial \bar{\bf y}_t}$ は softmax の微分を考えれば良く、

\begin{equation}
    \begin{split}
         \frac{\partial f_2({\bf v}_{i})}{\partial {\bf v}_{k}} &= \frac{\frac{\partial exp({\bf v}_i)}{\partial {\bf v}_k} \cdot \sum_j exp({\bf v}_{j}) - exp({\bf v}_i) \cdot exp({\bf v}_k)}{(\sum_j exp({\bf v}_{j}))^2} \\
                                                                &= \frac{\frac{\partial exp({\bf v}_i)}{\partial {\bf v}_k}}{\sum_j exp({\bf v}_{j})} - \frac{exp({\bf v}_i)}{\sum_j exp({\bf v}_{j})} \cdot \frac{exp({\bf v}_k)}{\sum_j exp({\bf v}_{j})} \\
                                                                &= \begin{cases}
                                                                    f_2({\bf v}_{i})(1 - f_2({\bf v}_{k})) & (i = k) \\
                                                                    - f_2({\bf v}_{i}) \cdot f_2({\bf v}_{k}) & (i \neq k)
                                                                \end{cases}
    \end{split}
\end{equation}

より、
\begin{equation}
    \begin{split}
        \frac{\partial {\bf y}_t}{\partial \bar{\bf y}_t} &= \left(
            \begin{array}{cccc}
            {\bf y}_{t1}(1 - {\bf y}_{t1}) & -{\bf y}_{t2}{\bf y}_{t1} & \ldots & -{\bf y}_{tN}{\bf y}_{t1} \\
            -{\bf y}_{t1}{\bf y}_{t2} & {\bf y}_{t2}(1 - {\bf y}_{t2}) & \ldots & -{\bf y}_{tN}{\bf y}_{t2} \\
            \vdots & \vdots & \ddots & \vdots \\
            -{\bf y}_{t1}{\bf y}_{tN} & -{\bf y}_{t2}{\bf y}_{tN} & \ldots & {\bf y}_{tN}(1 - {\bf y}_{tN})
            \end{array}
        \right) \\
                                                          &= - ({\bf y}_t \cdot {\bf y}_t - ({\bf y}_t \odot {\bf I}))
    \end{split}
\end{equation}

なお、${\bf I}$ は単位行列。

よって簡単のため $t = T$ のときについて考えると、

\begin{equation}
    \begin{split}
        \frac{\partial E}{\partial \bar{\bf y}_T} &= ({\bf y}_T \cdot {\bf y}_T - {\bf y}_T \odot {\bf I}) \cdot \frac{{\bf l}_{T}}{{\bf y}_T} \\
                                                  &= {\bf y}_T - {\bf l}_T \;\; (\because \sum_i {\bf l}_{ti} = 1)
    \end{split}
\end{equation}

以降は近いうちに追記予定。
