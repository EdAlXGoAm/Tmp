function extractTablesFromText(text: string) {
  const tables: any[] = [];
  const lines = text.split('<br/>');
  let currentTable: any = null;
  let lastWasHeader = false;
  lines.forEach((line) => {
    // if (line.trim() === '') return;

    const isTableLine = line.includes('|');
    if (isTableLine) {
      if (lastWasHeader) {
        currentTable.rows.push(line.split('|').map((cell) => cell.trim()));
      } else {
        if (currentTable && currentTable.rows.length > 0) {
          const containsPage = currentTable.headers.some((header: string) => header.includes('page')) ||
                               currentTable.rows.some((row: string[]) => row.some((cell: string) => cell.includes('page')));
          if (!containsPage) {
            tables.push(currentTable);
          }
        }
        currentTable = {
          headers: line.split('|').map((header) => header.trim()),
          rows: [],
        };
      }
      lastWasHeader = true;
    } else {
      lastWasHeader = false;
    }
  });

  if (currentTable && currentTable.rows.length > 0) {
    const containsPage = currentTable.headers.some((header: string) => header.includes('page')) ||
                         currentTable.rows.some((row: string[]) => row.some((cell: string) => cell.includes('page')));
    if (!containsPage) {
      tables.push(currentTable);
    }
  }

  return tables;
}

function convertTablesToHtml(tables: any[]) {
  return tables
    .map((table) => {
      let html = '<table border="1" style="border-collapse: collapse; width: 100%;">';
      html += '<thead><tr>';
      table.headers.forEach((header: string) => {
        html += `<th>${header}</th>`;
      });
      html += '</tr></thead>';
      html += '<tbody>';
      table.rows.forEach((row: any[]) => {
        html += '<tr>';
        row.forEach((cell: string) => {
          html += `<td>${cell}</td>`;
        });
        html += '</tr>';
      });
      html += '</tbody></table>';
      return html;
    })
    .join('<br/>');
}

export function identifyTablesAndInsertToQuill(pdfText: string, setPdfText: (prevText: string) => void) {
  const tables = extractTablesFromText(pdfText);
  const tablesHtml = convertTablesToHtml(tables);
  if (tablesHtml) {
    setPdfText(pdfText);
  }
  return tablesHtml;
}
