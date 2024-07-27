import { translateAllInOneStep } from '../scripts/translate.mts';

describe('Translation Consistency Tests', () => {
  test('Consistent translation across title, summary, and reactions', async () => {
    const input = {
      title: 'Test Title',
      summary: ['Summary point 1', 'Summary point 2'],
      reaction: ['Reaction point 1'],
      titleLang: 'en',
      summaryLang: 'en',
      reactionLang: 'en',
    };

    const output = await translateAllInOneStep(input);

    expect(output).toHaveProperty('title');
    expect(output).toHaveProperty('summary');
    expect(output).toHaveProperty('reaction');
    expect(output.title).toBe('Test Title');
    expect(output.summary).toEqual(['Summary point 1', 'Summary point 2']);
    expect(output.reaction).toEqual(['Reaction point 1']);
  });

  test('Translation consistency with different inputs', async () => {
    const inputs = [
      {
        title: 'First Test',
        summary: ['First summary'],
        reaction: ['First reaction'],
        titleLang: 'en',
        summaryLang: 'en',
        reactionLang: 'en',
      },
      {
        title: 'Second Test',
        summary: ['Second summary'],
        reaction: ['Second reaction'],
        titleLang: 'en',
        summaryLang: 'en',
        reactionLang: 'en',
      },
    ];

    const results = await Promise.all(inputs.map(input => translateAllInOneStep(input)));

    expect(results[0].title).toBe('First Test');
    expect(results[0].summary).toEqual(['First summary']);
    expect(results[0].reaction).toEqual(['First reaction']);

    expect(results[1].title).toBe('Second Test');
    expect(results[1].summary).toEqual(['Second summary']);
    expect(results[1].reaction).toEqual(['Second reaction']);
  });
});
