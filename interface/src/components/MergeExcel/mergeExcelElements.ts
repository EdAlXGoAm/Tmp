import { useState } from 'react';
import * as XLSX from 'xlsx';

export const useMergeExcel = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string>('');
  const [mergedFileName, setMergedFileName] = useState<string>('');
  const [column1, setColumn1] = useState<string>('');
  const [column2, setColumn2] = useState<string>('');
  const [newColumn, setNewColumn] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMerged, setIsMerged] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');
  const [workbook, setWorkbook] = useState<XLSX.WorkBook | null>(null);
  const [worksheetName, setWorksheetName] = useState<string>('');
  const [data, setData] = useState<any[]>([]);
  const [groupColumn, setGroupColumn] = useState<string>('');

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    setSuccessMessage('');
    setIsMerged(false);
    const uploadedFile = e.target.files?.[0];
    if (uploadedFile) {
      if (uploadedFile.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' &&
          uploadedFile.type !== 'application/vnd.ms-excel') {
        setError('Por favor, suba un archivo de Excel válido (.xlsx o .xls).');
        return;
      }
      setFile(uploadedFile);
      setFileName(uploadedFile.name);
      const reader = new FileReader();
      reader.onload = (evt) => {
        const binaryStr = evt.target?.result;
        if (typeof binaryStr === 'string' || binaryStr instanceof ArrayBuffer) {
          const wb = XLSX.read(binaryStr, { type: 'binary' });
          setWorkbook(wb);
          const wsName = wb.SheetNames[0];
          setWorksheetName(wsName);
          const ws = wb.Sheets[wsName];
          const jsonData = XLSX.utils.sheet_to_json(ws, { defval: '' });
          setData(jsonData);
        }
      };
      reader.onerror = () => {
        setError('Error al leer el archivo.');
      };
      reader.readAsBinaryString(uploadedFile);
    }
  };

  const handleMergeColumns = () => {
    if (!workbook || !worksheetName || !data.length) {
      setError('No se ha cargado correctamente el archivo de Excel.');
      return;
    }
    if (!column1 || !column2 || !newColumn || !groupColumn) {
      setError('Por favor, complete todos los campos de las columnas.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      const groupedData: Array<{ groupName: string; rows: any[] }> = [];
      let currentGroup: any[] = [];
      let currentGroupName: string = '';

      data.forEach((row) => {
        const groupValue = row[groupColumn];
        if (groupValue) {
          if (currentGroup.length > 0) {
            groupedData.push({ groupName: currentGroupName, rows: currentGroup });
          }
          currentGroupName = groupValue;
          currentGroup = [row];
        } else {
          currentGroup.push(row);
        }
      });

      if (currentGroup.length > 0) {
        groupedData.push({ groupName: currentGroupName, rows: currentGroup });
      }

      const updatedData: any[] = [];

      groupedData.forEach(group => {
        const mergedValues = group.rows.map(row => {
          if (!(column1 in row) || !(column2 in row)) {
            throw new Error('Una o ambas columnas especificadas no existen en el archivo.');
          }
          return `${row[column1]}=${row[column2]}`;
        });

        const mergedString = mergedValues.join(';');

        const firstRow = { ...group.rows[0], [newColumn]: mergedString };

        const { [column1]: _, [column2]: __, ...restFirstRow } = firstRow;

        updatedData.push(restFirstRow);
      });

      setData(updatedData);

      setIsMerged(true);
      setSuccessMessage('Las columnas se han combinado exitosamente.');
    } catch (err: any) {
      setError(err.message || 'Ocurrió un error al combinar las columnas.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!workbook || !worksheetName || !data.length) {
      setError('No hay datos para descargar.');
      return;
    }
    setIsLoading(true);
    try {
      const newWs = XLSX.utils.json_to_sheet(data);
      const newWb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(newWb, newWs, worksheetName);
      const wbout = XLSX.write(newWb, { bookType: 'xlsx', type: 'binary' });

      const buf = new ArrayBuffer(wbout.length);
      const view = new Uint8Array(buf);
      for (let i = 0; i < wbout.length; i++) {
        view[i] = wbout.charCodeAt(i) & 0xFF;
      }
      const blob = new Blob([buf], { type: 'application/octet-stream' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const newFileName = fileName.replace(/\.(xlsx|xls)$/, '') + '_merged.xlsx';
      a.download = newFileName;
      a.click();
      window.URL.revokeObjectURL(url);
      setMergedFileName(newFileName);
      setSuccessMessage('Archivo descargado exitosamente.');
    } catch (err: any) {
      setError('Error al descargar el archivo.');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    handleFileUpload,
    handleMergeColumns,
    handleDownload,
    fileName,
    mergedFileName,
    column1,
    column2,
    newColumn,
    setColumn1,
    setColumn2,
    setNewColumn,
    isLoading,
    error,
    successMessage,
    isMerged,
    groupColumn,
    setGroupColumn,
  };
}; 