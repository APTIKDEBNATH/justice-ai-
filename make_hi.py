import re

with open('debug_hi_template.html', 'r', encoding='utf-8') as f:
    val = f.read()

# Replace asset uuids
val = val.replace('13ba5071-d697-4522-a346-24292d3ca0e2', 'https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7SUc.woff2')
val = val.replace('c702bded-8274-4c3f-bee2-a3daa81f4cb1', 'https://fonts.gstatic.com/s/newsreader/v26/cY9VfjOCX1hbuyalUrK49dLac06G1ZGsZBtoBAbEJYQraA.woff2')
val = val.replace('4a89b424-c6f8-4adc-84b2-f8e537b2acfd', 'https://fonts.gstatic.com/s/notosansdevanagari/v33/TuG7UUFzXI5FBtUq5a8bjKYTZjtRU6Sgv3NaV_SNmI0b8QQCQmHN6jV_9qo.woff2')
val = val.replace('25e30a9a-6aed-433c-b854-02e1fcea1136', 'https://fonts.gstatic.com/s/notosansdevanagari/v33/TuG7UUFzXI5FBtUq5a8bjKYTZjtRU6Sgv3NaV_SNmI0b8QQCQmHN6jV_9qo.woff2')
val = val.replace('56b538c7-8c0e-4a5f-8b7a-496b891c7144', 'https://fonts.gstatic.com/s/notoserifdevanagari/v34/x3dNcl3IZKmUqiMk48ZHXJ5jwU-DZGRSaQ4Hh2dGyFzPLcQPVbnRH-NEMqTN.woff2')
val = val.replace('d287fe9b-1829-4a5c-8654-79b702bd0b3b', 'https://fonts.gstatic.com/s/notoserifdevanagari/v34/x3dNcl3IZKmUqiMk48ZHXJ5jwU-DZGRSaQ4Hh2dGyFzPLcQPVbnRH-NEMqTN.woff2')
val = val.replace('{{accent}}', '#1F4E79')
val = val.replace('<x-dc>', '').replace('</x-dc>', '')
val = val.replace('<sc-raw-select>', '<select>').replace('</sc-raw-select>', '</select>')
val = val.replace('sc-camel-view-box', 'viewBox')

with open('standalone_hi.html', 'w', encoding='utf-8') as out:
    out.write(val)
print("Wrote standalone_hi.html, length:", len(val))
