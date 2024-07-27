<h1 align="center">Heimdall</h1>

<div align="center">

summarizes HN in 30 Languages 💬

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fanaclumos%2Fheimdall.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fanaclumos%2Fheimdall?ref=badge_shield) [![news](https://github.com/anaclumos/heimdall/actions/workflows/news.yaml/badge.svg)](https://github.com/anaclumos/heimdall/actions/workflows/news.yaml)

</div>

<div align="center">

![Repobeats analytics image](https://repobeats.axiom.co/api/embed/a1c452e1ca6a2929a1bdea415fdd28a7b7dfb3e9.svg)

</div>

- Not seeing your language? Please leave us an issue!
- [العربية](https://hn.cho.sh/ar)
- [বাংলা](https://hn.cho.sh/bn)
- [Čeština](https://hn.cho.sh/cs)
- [Dansk](https://hn.cho.sh/da)
- [Deutsch](https://hn.cho.sh/de)
- [Ελληνικά](https://hn.cho.sh/el)
- [English](https://hn.cho.sh)
- [Español](https://hn.cho.sh/es)
- [Suomi](https://hn.cho.sh/fi)
- [Français](https://hn.cho.sh/fr)
- [עברית](https://hn.cho.sh/he)
- [हिंदी](https://hn.cho.sh/hi)
- [Magyar](https://hn.cho.sh/hu)
- [Bahasa Indonesia](https://hn.cho.sh/id)
- [Italiano](https://hn.cho.sh/it)
- [日本語](https://hn.cho.sh/ja)
- [한국어](https://hn.cho.sh/ko)
- [Nederlands](https://hn.cho.sh/nl)
- [Norsk Bokmål](https://hn.cho.sh/nb)
- [Polski](https://hn.cho.sh/pl)
- [Português](https://hn.cho.sh/pt)
- [Română](https://hn.cho.sh/ro)
- [Pусский](https://hn.cho.sh/ru)
- [Slovenčina](https://hn.cho.sh/sk)
- [Svenska](https://hn.cho.sh/sv)
- [தமிழ்](https://hn.cho.sh/ta)
- [ไทย](https://hn.cho.sh/th)
- [Türkçe](https://hn.cho.sh/tr)
- [Tiếng Việt](https://hn.cho.sh/vi)
- [简体中文](https://hn.cho.sh/zh-Hans)
- [繁體中文](https://hn.cho.sh/zh-Hant)

## Translation Process

To ensure consistency in translations across different sections of content, Heimdall utilizes a unified translation module. This module processes the title, summary, reaction, and translation in a single step using GPT-4o, significantly reducing the number of external calls and ensuring uniformity in translated terms across sections.

### Guidelines for Maintaining Consistency

- Use the `translateAllInOneStep` function from the `scripts/translate.mts` module for translating content.
- Provide the title, summary, and reactions along with their respective languages as parameters to the function.
- The module ensures terminology consistency across title, summary, and reaction by utilizing context management within the GPT-4o prompt.
- This approach helps maintain a coherent and consistent translation across different languages and sections of content.
