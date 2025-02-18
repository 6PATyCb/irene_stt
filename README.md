# irene_stt
Плагин для `Home Assistant`, позволяющий использовать [Ирины](https://github.com/janvarev/Irene-Voice-Assistant) в качестве STT (распознавания речи в текст). 

Для работы требуется [Ирина](https://github.com/janvarev/Irene-Voice-Assistant) запущенная в режиме `runva_webapi.py` и мой плагин [IreneVA_Willow_plugin](https://github.com/6PATyCb/IreneVA_Willow_plugin) версии не ниже 2.1, т.к. его эндпоинт `/api/willow` используется для преобразования голоса в текст.

## Как установить плагин

Установка происходит так же как это делается с любым сторонним плагином, т.е. через копирование папки `irene_stt` со всем его содержимым в каталог `custom_components` в HA. 

После копирования папки, выполните полную перезагрузку `Home Assistant`. Далее перейдите в раздел `Настройки` -> `Устройства и службы`, нажмите кнопку `Добавить интеграцию` и в поиске введите `Irene STT`. Далее укажите ссылку до запущенной Ирины, у меня она выглядит так:
```
https://192.168.133.252:5003
```
Теперь перейдите в раздел `Настройки` -> `Голосовые ассистенты` и там создайте нового ассистента или отредактируйте существующего. В разделе `Распознавание речи` можно будет выбрать `Irene STT`. Обращаю внимание, что плагин собран для работы с русским языком и если вдруг вы выбрали еще какой-то язык для ассистента, то плагин не будет отображаться в выпадающем списке. 




