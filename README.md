# AntiAlertstorm
## 概要
この`AntiAlertstorm`は`Istio`を導入した`Sock Shop`に対してアラートソフトウェアです．  
  
こちらを参考[Istioを導入したSock Shop](https://qiita.com/hikida621/items/ddebe34566d5fce913fc)  
  
`Sock Shop`の各サービス間の応答時間`3000ms`をサービスの異常とし，これに備えるためのアラートを出します．  
  
## 使用方法
`alert/mail.py`にメールアドレスを入力します．  
  
`main.py`にcsvファイルをを出力する`path`を入力します．  
  
`main.py`を実行することでAntiAlertstormを起動します．  
