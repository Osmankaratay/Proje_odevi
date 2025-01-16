
# Görevli Dağıtım

Bu proje Yakin Tiyatronun bir aylık ışık, ses ve kafe görevlileri dağıtımı için özel yazılmıştır.

Excel tablosu linki: https://docs.google.com/spreadsheets/d/16Q-lSq-tW2A3j_wbicM5cLPYx45A_ErCGAlr0RGjZP4/edit?usp=sharing

Değiştirilen tablo: Görev Listesi 24-25
Kontrol tablo: Kontrol sayfası


## API Kullanımı

#### Tüm öğeleri getir

```http
  GET /api/items
```

| Parametre | Tip     | Açıklama                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Gerekli:** AIzaSyBgfgTk6DfMkSGsCvOJr7RlOX1eE3YWDMg |

#### Öğeyi getir

```http
  GET /api/items/${id}
```

| Parametre | Tip     | Açıklama                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Gerekli:** 16Q-lSq-tW2A3j_wbicM5cLPYx45A_ErCGAlr0RGjZP4 |

#### Bir aralıktan veri okuma
    spreadsheets().values().get
    
    Parametreler:
        spreadsheetId: Google Sheet'in ID'si.
        range: Hücre aralığı

#### Veri yazma veya güncelleme
    spreadsheets().values().update

    Parametreler:
        spreadsheetId: Google Sheet'in ID'si.
        range: Güncellenecek hücre aralığı.
        valueInputOption: Verilerin nasıl işleneceğini belirtir (USER_ENTERED veya RAW).
        body: Yazılacak veriler.

#### API kullanımı için gerekli .json dosyası
    {
    "type": "service_account",
    "project_id": "yakingorev001",
    "private_key_id": "54de86d09e20fe61e4ece490f8503716ec782e14",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMy5wYtDe+Me6W\nGqIDFRQZNDWLS3nzQWVnAKL23UNrQeG5GtMJ44/poMSSNMvDnAtLBs72QLLsYIu0\nK3b2xatkPIuyQyiafN03VpckS1th933fVm3CSNb66hkkMQzF9txTNTwUj8hUleOp\n2w7jp0dlGNWy6usR2YoMVkSBldqUSolAL/vFaEQyJqrbj26IgaX1tA+r/iAJYrjA\nzcak8naHgJmASjUamBp4QSghHzfbymtelzRmbQbIynxqPA1z0B8BPykobp5kjmbl\n2OKvsjW24goVsefYL122n5t0ha5sk3Y+cMp9Al5UvDu7GEXyWEBQMUn6qhzqPIdj\npR72iRiTAgMBAAECggEABhfw1xNVrUUTEkhMlcbkyDMzfKeMQ16ow73TG4FN5j0Z\nmEZiDSNGPu9XqfoELhfQhjT3p4AZUss0nPHGImWTSfI7PdydsqsQcfsTmDLdzzZr\n+l85+NPuAZ1BjkAfXyyPNbKZzQrSLSIgmgc4lDGAAFQS17YBtJBCeUd/1lM9I7he\nZBK5pbgvcJ4ltdHOElxJCpa2MFBuYS3AGaAbk+Z5TCERzMr/ZenHGEwn1hVJqkX2\na5p0GvqjfnPn43jF/NeOVHzW3jiJPG3aIiQMa+doDFQsdj4GElextj8yNjgCVzh5\nQUXdJUaUzPvhjZ2YJVdUaiVg9buew33yQievNn5wkQKBgQDxTAZ9DcDBs+Pr7UEr\nKVd1z8zSMt4+1+pBMWocrhU2w2EE6VzfsVTqZCZVN+k2ICTIZCB8/xH+pQg2Nlq1\nnJ5jT+I9FGeK8jhVv0gkuZvkFjXMUy/Oi90t5DnpG9pilGHTzgGp0LXbZuNTfCZS\nKPxnnKl7roqZwrPKIUIiV764ZwKBgQDZRjK4r4ls24ZxvcuFQOxNLYzQ5kUSm0RP\nu3kJRibfU29owmhzfImvaYlYhlbcPnPrw/+M8V3bn4FgRzkcSf6kUaLZTAgykKaZ\nr1ZhBRNv23VC9NtUU7QdtnI9UdA+jgs83DN4e39wWBijyGDJINyI81xWbBRrYK4O\nYNoC5f2y9QKBgClPbrzyIdIHzjmSANo21bZhwRsrgkkYBg7rOtN2KkOZ535DxZa2\ncWc/hiCI1fBiSGnWWomL0bTa5DED1TvKeINgJcd3OtLa7TIg8WT4Mew2sTct9r1R\nzKgSrqduEVFXPfhZCIfeJ4RMdRbR5m2ifrPuakW2eBwi7UzprLzccNZ5AoGAZtO6\nHX215DbgoePY9e+L5dqw0gyok+23nqRy29i/fOHX0BRxqnY+Ey43OhYZ9ZH4+pN/\n1gxFBzOt3wrWFHVQdiPMllpNZuDed81ra+8jC8Uo8c9AHeCfVZCK8EpP68r9tofg\nNBz+awTGZHzokUdkF8xU3vG3mDnhJhzgEI8YSiECgYEAg/U25ro1rAvrrMvQmcjB\ng4EyKQyciDKP5/9CbIHMUZhomeqHVO4LGuxtFD3Cy5DGr4wpYEotOUHi9A1jOk2c\nlL/eqBrtF8eumd+KyNjaydbxhmHfJ67Zi0ns8W6KFsf7UyXG9FQ2wKSd6xwnoE3T\n1TZZAcspqP5hEHTmNpdE7Dk=\n-----END PRIVATE KEY-----\n",
    "client_email": "yakin-449@yakingorev001.iam.gserviceaccount.com",
    "client_id": "111834435595437641566",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/yakin-449%40yakingorev001.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }






  
## Anahtar Özellikler
    Google Sheets Entegrasyonu:
        API etkileşimi için googleapiclient.discovery ve google.oauth2 kullanır.
        Bir Google Sheets belgesinden belirli aralıkları okur ve günceller.
    
    Yerelleştirme:
        Doğru dizgi işleme için Türkçe UTF-8 yerel ayarlarını işleyecek şekilde yapılandırılmıştır.
    
    …Rol Atama Mantığı:
        Uzmanlık ve yasakları dikkate alarak dinamik olarak roller atar.
        Ayrıntılı rol dağılımı istatistikleri oluşturur.
    
    Çıktı:
        Yeni rol atamaları ve sayıları ile Google Sheets'i günceller.


## Kullanım Talimatı
Gerekli Python kütüphaneleri: 
    
    requests, googleapiclient, google.oauth2, numpy, pandas.
    
    Eksikse pip ile yükleyin:
        pip install requests google-api-python-client google-auth numpy pandas

Google API Kurulumu:

    Bir Google Cloud projesi oluşturun ve Sheets API'yi etkinleştirin.
    Hizmet hesabı kimlik bilgileriyle bir keys.json dosyası indirin.
    keys.json dosyasını script ile aynı dizine yerleştirin.

Çevre Yapılandırması:

    SPREADSHEETS_ID'yi Google Sheets ID'niz ile güncelleyin.
    Gerekli tüm aralıkların ('Kontrol sayfası'!C4, vb.) elektronik tabloda mevcut olduğundan emin olun.
## Çalışma Mantığı
1. Yetkilendirme:

    keys.json kullanarak Google Sheets erişimini yetkilendirir.

2. Veri Çıkartma:

    Belirli aralıklardan oyun detaylarını, oyuncuları, rolleri ve yasakları yükler.

3. Rol Atama:

    Her oyun tarihi için üyelere roller atar, yasakları ve uzmanlık limitlerini dikkate alır.

4. Tablo Güncelleme:

    Güncellenmiş rol atamalarını ve sayılarını belirtilen tablo aralıklarına gönderir.

5. Uygulama:

    "Signal" değişkenini sürekli kontrol eder ve aktif olduğunda verileri işler.
## Anahtar Fonksiyonlar
1. Authorization:

    authorize_google_sheets(): Google Sheets API ile kimlik doğrulama yapar.

2. Spreadsheet Operations:

    load_spreadsheet_ranges(): Aralık değerlerini okur: signal, dates, members...
    extract_spreadsheet_values(): Belirli aralıktaki veriyi okur.

3. Play Management:

    create_play(play): Oyun detaylarını yapılandırılmış verilere çıkarır.
    creating_Play_objects(...): Çıkarılan detayları Oyun nesnelerine dönüştürür.

4. Role Assignment:

    play_date(...): Üyelerin rollerinin atanmasını yönetir.
    assign_role(...): Işık veya ses özel rollerini atar.

5. Banned Members:

    extract_banned(...): Belirli tarihler için yasaklı üyeleri filtreler.
    _banned class: Yasaklı üyeleri ve onların müsait olmadığı tarihleri temsil eder.

6. Data Export:

    send_to_spreadsheet(...): İşlenmiş verileri tekrar elektronik tabloya yazar.

