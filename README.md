# Norwegian Police Log for Home Assistant

**Status: Beta – Testing encouraged**

This Home Assistant integration displays real-time police reports directly from [Politiet.no](https://www.politiet.no) using their public API.

---

## 📦 HACS Installation

This integration is not in the default HACS store yet, but it's easy to install manually through HACS as a custom repository.

### ✅ Step-by-step:

1. In Home Assistant, go to **HACS > Integrations**
2. Click the **three dots menu (⋮)** in the top right > **Custom repositories**
3. Add the following repository URL: https://github.com/feddiriko/HomeAssistant_Norwegian_Policelog ( Select **Integration** as the category. )
4. After saving, go back to **HACS > Integrations**  
5. Search for `Norwegian Policelog` and install it.
6. Restart Home Assistant.
7. Add the integration via UI: Settings > Devices & Services > Add Integration


Or click this button:

[![Open in Home Assistant](https://my.home-assistant.io/badges/integration.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=norwegian_policelog)

---

## 🔍 Features

- Live updates of latest police logs from **Politiet.no**
- Filter by **district** and optionally **municipality**
- Updates every 60 seconds
- Native UI setup
- Supports all Norwegian police districts

---

## 🛠 Configuration

- **District** is required
  
Districts:
- Oslo
- Øst
- Innlandet
- SørØst
- Agder
- SørVest
- Vest
- MøteOgRomsdal
- Trøndelag
- Nordland
- Troms
- Finnmark

---

## 📝 License

MIT License

Created by [@feddiriko](https://github.com/feddiriko)











[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/feddiriko)
