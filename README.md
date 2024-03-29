# Home Assistant интеграция для подключения WiFi-реле напряжения (счетчиков) от компании ["Новатек-Электро"](https://novatek-electro.com/ru/)
Модели поддерживаемого оборудования:
* EM-125
* EM-126T
* EM-125S
* EM-126TS
* [EM-129](https://novatek-electro.ru/catalog/ustroystva-s-wi-fi-upravleniem/wi-fi-schetchik-elektroenergii-s-funktsiey-zashchity-i-upravleniya-em-129/)

## Подключение к Home Assistant
В домашнем каталоге Home Assistant создать каталог с именем *custom_components*, если он еще не существует, перейти в него и выполнить команду `git clone https://github.com/vedga/novatek.git`.

В файле *configuration.yaml* добавляем строчку
```

novatek: !include_dir_named conf/novatek/

```
В домашнем каталоге Home Assistant создаем каталог с именем *conf/novatek*, а в нем текстовой файл *devices.yaml* (имя файла фиксированное: по нему Home Assistant определяет, к какой категории отнести содержимое). Внутри описываем все подключаемые устройства:
```
meterA:
  host: "192.168.0.100"
  password: "super_secret"
meterB:
  host: "192.168.0.101"
  password: "super_secret"
```
где *meterA* и *meterB* - имена устройств, которыми будет оперировать Home Assistant, *host* - IP адрес конкретного устройства, *password* - пароль для доступа к соответствующему устройству (задается при программировании устройства).
После этого перезапускаем Home Assistant и устройства должны стать доступны для использования.

![image](https://user-images.githubusercontent.com/15801596/138332306-8cda4557-03ff-4aff-ba88-699adfd89714.png)

В последних версиях Home Assistant появилась возможность учета электроэнергии. Данная интеграция также поддерживает эту возможность:

![image](https://user-images.githubusercontent.com/15801596/138332392-ee9f83f7-ca31-49db-9471-3732ff2911f0.png)

## Реализованные возможности
* *novatek_имяустройства_voltage* сенсор напряжения
* *novatek_имяустройства_current* сенсор проходящего тока
* *novatek_имяустройства_power* сенсор текущей мощности
* *novatek_имяустройства_energy* сенсор потребляемой энергии
* *novatek_имяустройства_frequency* сенсор текущей частоты сети

## Известные проблемы
**При входе в Web-интерфейс устройства пропадают данные в Home Assistant. При работающем Home Assistant теряется авторизация на Web-интерфейсе устройства.**

Это поведение обусловлено тем, что устройства поддерживают только один пользовательский сеанс через Web-интерфейс (UI-интерфейс устройства и API, через который работает интеграция с Home Assistant).

**Workaround:** перед входом в Web-интерфейс устройства отключить его в интеграции с перезапуском Home Assistant.

**Если в устройстве настроено получение адреса через DHCP, то через какое-то время доступ к нему пропадает**

Данная проблема разработчику устройств известна, но еще не исправлена. В момент обновления IP-адреса по DHCP устройство теряет информацию о default gateway, поэтому становится недоступным из других сегментов IP-сетей (но остается доступным из сегмента, попадающего под сетевую маску выделенного адреса).

**Workarounds:**

* Использовать "плоскую" сеть: управляющий компьютер и само устройство должно находиться в одном сегменте IP-сети
* На маршрутизаторе на интерфейсе, к которому подключено устройство, настроить NAT таким образом, чтобы IP-пакеты к устройству имели в качестве source IP адрес интерфейса маршрутизатора, находящегося в том же сегменте сети, что и само устройство.
* Продолжить пинать [представителя производителя](https://mysku.ru/profile/Broomber) чтобы они все-таки пофиксили данную проблему

## API от производителя оборудования
Можно посмотреть [здесь](https://htmlpreview.github.io/?https://github.com/vedga/novatek/blob/main/API/WebApi_EM-125_126_129_.html).

