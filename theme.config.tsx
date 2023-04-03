import React from 'react'
import { DocsThemeConfig, useConfig } from 'nextra-theme-docs'
import { useRouter } from 'next/router'

const config: DocsThemeConfig = {
  logo: <><strong>hn.cho.sh</strong><sup>beta</sup></>,
  project: {
    link: 'https://github.com/anaclumos/hn.cho.sh',
  },
  docsRepositoryBase: 'https://github.com/anaclumos/hn.cho.sh/blob/main/',
  footer: {
    text: (
      <span>
        MIT {new Date().getFullYear()} ©{' '}
        <a href="https://cho.sh" target="_blank">
          Sunghyun Cho
        </a>
        .
      </span>
    ),
  },
  editLink: {
    text: 'Edit This Page on GitHub',
  },
  toc: {
    float: true,
  },
  // seo
  useNextSeoProps() {
    const { frontMatter } = useConfig()
    let title = frontMatter.top_news ?? 'The Latest Tech News 🗞️ in Your Language 💬 in Your Inbox 📭'
    return {
      titleTemplate: `${title} — hn.cho.sh`,
    }
  },
  head: () => {
    let { asPath, defaultLocale, locale } = useRouter()
    const { frontMatter } = useConfig()
    const url = `https://hn.cho.sh/${locale === defaultLocale ? '' : locale}${asPath}`
    let title = frontMatter.top_news ?? 'The Latest Tech News 🗞️ in Your Language 💬 in Your Inbox 📭'
    let subheading = frontMatter.localized_date ?? 'hn.cho.sh'
    return (
      <>
        <title>{title ?? 'hn.cho.sh'}</title>
        <meta property="og:url" content={url} />
        <meta property="og:title" content={title ?? 'hn.cho.sh'} />
        <meta
          property="og:image"
          content={`/api/og?title=${encodeURIComponent(title)}&subheading=${encodeURIComponent(subheading)}`}
        />
      </>
    )
  },
  themeSwitch: {
    useOptions() {
      return {
        light: 'Light',
        dark: 'Dark',
        system: 'System',
      }
    },
  },
  i18n: [
    { locale: 'bg', text: 'български (bg)' },
    { locale: 'cs', text: 'Čeština (cs)' },
    { locale: 'da', text: 'Dansk (da)' },
    { locale: 'de', text: 'Deutsch (de)' },
    { locale: 'el', text: 'Ελληνικά (el)' },
    { locale: 'en', text: 'English (en)' },
    { locale: 'es', text: 'Espanya (es)' },
    { locale: 'et', text: 'Eesti (et)' },
    { locale: 'fi', text: 'Suomi (fi)' },
    { locale: 'fr', text: 'Français (fr)' },
    { locale: 'hu', text: 'Magyar (hu)' },
    { locale: 'id', text: 'Bahasa Indonesia (id)' },
    { locale: 'it', text: 'Italiano (it)' },
    { locale: 'ja', text: '日本語 (ja)' },
    { locale: 'ko', text: '한국어 (ko)' },
    { locale: 'lt', text: 'Lietuvių (lt)' },
    { locale: 'lv', text: 'Latviešu (lv)' },
    { locale: 'nb', text: 'Bokmål (nb)' },
    { locale: 'nl', text: 'Nederlands (nl)' },
    { locale: 'pl', text: 'Polski (pl)' },
    { locale: 'pt', text: 'Português (pt)' },
    { locale: 'ro', text: 'Română (ro)' },
    { locale: 'ru', text: 'Русский (ru)' },
    { locale: 'sk', text: 'Slovenčina (sk)' },
    { locale: 'sl', text: 'Slovenščina (sl)' },
    { locale: 'sv', text: 'Svenska (sv)' },
    { locale: 'tr', text: 'Türkçe (tr)' },
    { locale: 'uk', text: 'Українська (uk)' },
    { locale: 'zh', text: '中文 (zh)' },
  ],
}

export default config
