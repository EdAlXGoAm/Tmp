import React from 'react';
import styles from './mergeExcel.module.css';
import { useMergeExcel } from './mergeExcelElements';
import { Button, TextField, Typography, CircularProgress } from '@mui/material';

const MergeExcel: React.FC = () => {
  const {
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
  } = useMergeExcel();

  return (
    <div className={styles.container}>
      <Typography variant="h4" gutterBottom>
        MergeExcel
      </Typography>

      <div className={styles.section}>
        <input
          type="file"
          accept=".xlsx, .xls"
          onChange={handleFileUpload}
          className={styles.fileInput}
        />
        {fileName && <Typography variant="subtitle1">Archivo seleccionado: {fileName}</Typography>}
      </div>

      <div className={styles.section}>
        <TextField
          label="Nombre de la Columna de Grupo"
          value={groupColumn}
          onChange={(e) => setGroupColumn(e.target.value)}
          className={styles.input}
        />
        <TextField
          label="Nombre de la Primera Columna"
          value={column1}
          onChange={(e) => setColumn1(e.target.value)}
          className={styles.input}
        />
        <TextField
          label="Nombre de la Segunda Columna"
          value={column2}
          onChange={(e) => setColumn2(e.target.value)}
          className={styles.input}
        />
        <TextField
          label="Nombre de la Nueva Columna"
          value={newColumn}
          onChange={(e) => setNewColumn(e.target.value)}
          className={styles.input}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleMergeColumns}
          disabled={
            isLoading ||
            !fileName ||
            !column1 ||
            !column2 ||
            !newColumn ||
            !groupColumn
          }
        >
          {isLoading ? <CircularProgress size={24} /> : 'Combinar Columnas'}
        </Button>
      </div>

      {isMerged && (
        <div className={styles.section}>
          <Button variant="contained" color="success" onClick={handleDownload}>
            Descargar Archivo Modificado
          </Button>
          <Typography variant="subtitle1">Archivo modificado: {mergedFileName}</Typography>
        </div>
      )}

      {error && (
        <Typography variant="body1" color="error">
          {error}
        </Typography>
      )}

      {successMessage && (
        <Typography variant="body1" color="primary">
          {successMessage}
        </Typography>
      )}
    </div>
  );
};

export default MergeExcel; 