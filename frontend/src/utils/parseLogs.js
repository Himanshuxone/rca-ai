export function parseLogLines(content) {
  const lines = content.split("\n").filter(Boolean);
  const parsed = [];

  const logRegex = /^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*?)\s+in component (\S+)/;

  for (const line of lines) {
    const match = logRegex.exec(line);
    if (match) {
      parsed.push({
        timestamp: match[1],
        level: match[2],
        message: match[3],
        component: match[4],
      });
    }
  }

  return parsed;
}
