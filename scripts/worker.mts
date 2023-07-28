import fs from 'fs'

import { updateHN } from './update.mjs'
import { collect } from './collect.mjs'
import { Story } from './type.mjs'
import { summarize } from './summarize.mjs'
import { LinguineList } from './linguine.mjs'
import { translate } from './translate.mjs'
import { scheduleNewsletter } from './newsletter.mjs'

const main = async () => {
  let stories: Story[] = await updateHN()

  // day in YYYY-MM-DD format
  const day = new Date().toISOString().split('T')[0]
  const path = `./records/${day}/${day}.en.json`

  if (!fs.existsSync(path)) {
    fs.mkdirSync(`./records/${day}`, { recursive: true })
  } else {
    stories = JSON.parse(fs.readFileSync(path, 'utf8'))
  }

  // this is to throttle the requests
  for (let i = 0; i < stories.length; i++) {
    if (!stories[i].originBody) {
      stories[i].originBody = await collect(stories[i].originLink)
    } else {
      console.log('💘 Body Exists\t', stories[i].title)
    }
    if (!stories[i].commentBody) {
      stories[i].commentBody = await collect(stories[i].commentLink)
    } else {
      console.log('💘 Comm Exists\t', stories[i].commentLink)
    }
  }

  stories = await Promise.all(
    stories.map(async (s) => {
      return summarize(s)
    })
  )

  // locale -> Stories map
  const localeStories = {}

  for (let i = 0; i < LinguineList.length; i++) {
    const locale = LinguineList[i]
    if (fs.existsSync(`./records/${day}/${day}.${locale}.json`)) {
      console.log('💘 Tran Exists\t', locale)
      localeStories[locale] = JSON.parse(
        fs.readFileSync(`./records/${day}/${day}.${locale}.json`, 'utf8')
      )
      continue
    }
    localeStories[locale] = await Promise.all(
      stories.map(async (s) => {
        return {
          ...s,
          title: await translate([s.title], 'en', locale)[0],
          originSummary: await translate(s.originSummary, 'en', locale),
          commentSummary: await translate(s.commentSummary, 'en', locale),
        }
      })
    )
    console.log('📝 Writing\t', locale)
  }

  for (let i = 0; i < LinguineList.length; i++) {
    const locale = LinguineList[i]
    fs.writeFileSync(
      `./records/${day}/${day}.${locale}.json`,
      JSON.stringify(localeStories[locale], null, 2)
    )
  }
  await scheduleNewsletter(localeStories)
}

main().then(() => process.exit(0))
