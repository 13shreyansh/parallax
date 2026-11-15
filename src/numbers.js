// Grouped numbers such as "8 260" must never break across lines.
export const keepNumbers = s => s.replace(/(\d)[  ](?=\d{3}(?!\d))/g, '$1 ');
