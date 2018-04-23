Title: Getting Things Done with Vim
Tags: Vim, Lifehack
Date: 2018-04-22 16:00 
Modified: 2018-04-22 16:00
Slug: Getting_Things_Done_with_Vim
Authors: guchio3
Summary: 


# 概要
４月から社会人として働いているのですが、TODO 管理の方法として [GTD (Getting Things Done)](https://ja.wikipedia.org/wiki/Getting_Things_Done) を教わったので Vim で運用してみようとした際のメモ。

Vim で GTD を管理するプラグインとして [phb1/gtd.vim](https://github.com/phb1/gtd.vim) が良さげだったので今回はこれを利用した。以下の記事は基本 `:help gtd.vim` を参考に記述。

まず、私は NeoBundle で Vim のプラグイン管理をしているので、上記のサイトに紹介されている基本設定を参考に .vimrc を次のように設定した。`filetype plugin on` により、`.gtd` ファイルを Gtd filetype として認識してプラグインの挙動を制御できる。`.gtd` はデフォルトで vim に認識してもらえなかったので、`au ~` の部分でこれを指定しており、また `let g:gtd#dir` で GTD を管理するディレクトリを指定している。(`~/workspace/gtd/notes/` の部分は適宜変更してください。)

    :::bash
    "" GTD (Getting Things Done)
    NeoBundle 'phb1/gtd.vim'
    au BufRead,BufNewFile *.gtd set filetype=Gtd
    filetype plugin on
    let g:gtd#dir = '~/workspace/gtd/notes/'

次に、Vim 上で次のコマンドを利用し、`.gtd` ファイル を作成。

    :::bash
    :GtdNew

すると次のような `.gtd` ファイルが日時に応じて `~/workspace/gtd/notes/` 以下に自動生成される。

    :::bash
    =
    @
    !

`.gtd` ファイルにおいて、`=` が title、`@` が context、`!` が action、`#` (これは上記のファイルには存在しないが) が hashtag を示す。初期設定では `:GtdNew` により生成される `.gtd` ファイルは上記のように簡素なものだが、`let g:gtd#default_context = 'hogehoge'` や `let g:gtd#default_action = 'fugafuga'` などと .vimrc をいじることでテンプレートを作成できる。


<br>
<br>
# GTD の運用を設計
GTD の運用には幾つものやり方があり、それぞれの個人にとって最適なやり方を見つける必要がある。今回は[このサイト](https://postd.cc/gtd-in-15-minutes/)を参考に簡単な運用法を設計してみた。

まず、今回使う context, action, hashtag を次のように設定した。

### context (行動を起こす状況を定義)
 * @work
     * 仕事でやること
 * @home
     * 家でやること

### action (タスクを分類)
 * !inbox
     * アイデアやタスク
 * !todo
     * すぐに行うタスク
 * !scheduled-YYYYMMDD
     * ある特定の日行うタスク ("その日までにやる"ものは書いてはダメ。)
 * !someday
     * いつかやるタスク
 * !delegate
     * 他者に委託したタスク
 * !archive
     * 実行し終わったタスク
 * !trash
     * 実行するのをやめたタスク (単純に `.gtd` ファイルを消しても良いが、この action を使っておいておくことが可能)

### hashtag (２つ以上のタスクにより構成される大枠のタスク)
 * 場合によって様々

上記の設定を用い、今回は次のワークフローでタスクを分類して GTD を実現する。

---
 1. 思いつくアイデア、タスクを全て洗い出し、!inbox に分類
 2. 実現可能か否かを判定
    * 実現可能な場合 3. に進む
    * 実現不可能な場合 !trash に分類
 3. 2 分で消化可能なタスクかを判定
    * 消化可能な場合、即座に消化して !archive に分類
    * 消化不可能な場合、4. に進む
 4. 他者に任せるか否かを判定
    * 任せる場合、!delegate に分類
    * 任せない場合、5. に進む
 5. 実行する日を指定するか否かを判定
    * 可能な場合、6. に進む
    * 不可能な場合、!someday に分類
 6. 実行する日が本日か否かを判定
    * 本日の場合、!todo に分類
    * 本日でない場合、!scheduled-YYYYMMDD に分類 
---
<!--GTD を運用する際、週次レビューをすることが推奨されます。週次レビューでは各プロジェクトに最低１つは-->

また、Inbox にいれるアイデア、タスクを想起させるために、トリガーリスト[ (例えばこれ)](http://www.itmedia.co.jp/bizid/articles/0607/14/news064.html) が利用される場合がある。今後 GTD 運用していく上で利用したい。



<br>
<br>
# phd1/gtd.vim を用いた運用例
まず、`GtdNew` で `.gtd` ファイルを生成する。この際に設定次第でデフォルトで context と action を埋めて置くことができる。私は次のように設定した。

    :::bash
    let g:gtd#default_context = 'work'
    let g:gtd#default_action = 'inbox'

まずはこの生成されるファイルに思いつくタスク、アイデアを記入するという動作を次のように行い、すべて出しつくすまでこれを繰り返す。

    :::bash
    =MTG 設定する
    @work
    !inbox

    山田さんとの MTG を設定し、チームに招待メールを送る。

次に、`:Gtd !inbox` コマンドで検索を行う。`:Gtd {formula}` コマンドでは `{formula}` の部分には AND や OR で検索条件を指定可能であり (他にも NOT、日付、キーワードなど様々な条件を指定可能)、例えば !inbox AND !todo、!inbox OR !todo は `!inbox !todo`、`!inbox + !todo` のように表現される。() を用いてより複雑な条件を指定することも可能である。なお、検索結果に出てくる `[  ]` という記号はチェックボックスの様で紛らわしいが、`[*]` で添付ファイルが存在することを表現するための記号である。

その後、検索結果画面でタスク一覧を確認し、各タスクを先程説明したワークフローに従って分類していく。分類は原始的で、!inbox を !todo に書き換えるなどして対応する。検索結果画面から各タスクには Enter で飛べる (キーは設定可能)。

ちなみに、この検索は他にも `GtdReview` によっても可能であり、このコマンドは設定ファイルに指定された特定の検索条件で検索を行う。毎日のタスク管理に最適。私は次のように設定した。

    :::bash
    let g:gtd#review = [
        \ '!inbox',
        \ '!todo',
        \ '!scheduled-'.strftime("%Y%m%d"),
        \ '!someday',
        \ ]

検索、編集後、検索結果画面は自動で編集後の状態にならないため、`:GtdRefresh` コマンドを走らせ、うまく編集できたかどうかを確認。あとは TODO を消化しつつ、終わり次第 `!archive` に入れていく作業！

なお、最終的に `.vimrc` の設定は次のとおりになった。
他にも `let g:gtd#cache = 1` とすればキャッシュを活用して高速に処理をしてくれるなど色々と設定はあるが、詳細は `:help gtd.vim` を参照。

    :::bash
    "" GTD (Getting Things Done)
    NeoBundle 'phb1/gtd.vim'
    au BufRead,BufNewFile *.gtd set filetype=Gtd
    filetype plugin on
    let g:gtd#dir = '~/workspace/gtd/notes/'
    let g:gtd#default_context = 'work'
    let g:gtd#default_action = 'inbox'
    let g:gtd#review = [
        \ '!inbox',
        \ '!todo',
        \ '!scheduled-'.strftime("%Y%m%d"),
        \ '!someday',
        \ ]

以上！
