## 0.4.1 (November 12, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. OutPortPahoPubSecureモジュールが正常に動作しない問題を修正

## 0.4.0 (November 12, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. OutPortPahoPublisherおよびOutPortPahoPubSecureモジュールに対して、MQTTプロトコル ver.3.1.1中の'Retain'と'Will'2つの機能を実装
1. 1.に伴い、MQTTクライアントモジュールであるPahoPublisherとPahoPubSecureの機能更新
1. その他全モジュールのMinor correction

## 0.3.0 (November 5, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. MQTTクライアントモジュールのうち、セキュア通信機能付きモジュール（PahoPubSecureまたはPahoSubSecure）をセキュア通信機能なしモジュール（PahoPublisherまたはPahoSubscriber）から継承するように修正
1. __init__ファイルの修正と、これに伴う各モジュールの修正

## 0.2.5 (October 1, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. 全モジュールにおけるプロパティname（key）"port"を"msport"に変更

## 0.2.4 (October 1, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. OutPortPahoPubSecureおよびInPortPahoSubSecureモジュールのrtc.confに入力したプロパティを読み込めないエラーを修正

## 0.2.3 (October 1, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. OutPortPahoPubSecureおよびInPortPahoSubSecureモジュールのMinor correction

## 0.2.2 (September 27, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. OutPortPahoPublisherおよびOutPortPahoPubSecureモジュールに対して、max inflight messagesに関する新たなプロパティを追加
1. 1.に伴い、MQTTクライアントモジュールであるPahoPublisherとPahoPubSecureの機能更新
1. InPortPahoSubSecureモジュールのMinor update

## 0.2.1 (September 19, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュール
1. ver.0.2.0で行った修正を同様に適用
1. OpenRTM-aist ver.1.2.0以降であれば、rtc.confにて"manager.components.preconnect"指定から、通信モジュールに関連するプロパティの事前設定できるように変更

## 0.2.0 (September 18, 2020)
OpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
1. "dataport"から階層化された名前空間に対応できるよう関数findPropを追加
1. 1.を利用した機能追加で、rtc.confにて"manager.components.preconnect"指定から、通信モジュールに関連するプロパティの事前設定できるように変更

## 0.1.0 (September 15, 2020)
OpenRTM-aist ver.1.2.1以前(Python2系）対応MQTT通信モジュールおよびOpenRTM-aist ver.1.2.2以降(Python3系）対応MQTT通信モジュール
* 初期バージョンリリース
