import React, { useState, useEffect } from 'react';
import styles from '../../styles/ContentForm.module.css';
import { ContentFormElements } from '../../constants/forms/contentFormElements';
import { RowForm } from '../../utils/formatUtils';
import { Modal } from '@mui/material';

interface ContentFormProps {
  elementToEdit: { key: string, value: any } | null;
  onCleanData: () => void;
  isOpenExternal: boolean;
  setIsOpenExternal: React.Dispatch<React.SetStateAction<boolean>>;
  updateContent: (key: string, value: any) => void;
  createContent: (value: string) => void;
}

const ContentForm: React.FC<ContentFormProps> = ({
  elementToEdit,
  onCleanData,
  isOpenExternal,
  setIsOpenExternal,
  updateContent,
  createContent
}) => {
  const {
    isOpen, setIsOpen,
    error, setError,
    loading, setLoading,
    formData, setFormData,
    handleClose,
    handleChange,
    handleSubmit
  } = ContentFormElements({ elementToEdit, onCleanData, updateContent, createContent, setIsOpenExternal });

  useEffect(() => {
    if(elementToEdit) {
      setFormData({ key: elementToEdit.key, value: elementToEdit.value });
    }
  }, [elementToEdit]);

  useEffect(() => {
    setIsOpen(isOpenExternal);
  }, [isOpenExternal]);

  return (
    <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
      <h2>{elementToEdit ? 'Edit Content' : 'Create Content'}</h2>
      <form onSubmit={handleSubmit}>
        <RowForm>
          <label>Content</label>
          <div className={styles.statesListBox}>
            <button className={`${styles.statesListBoxButton} ${styles.statesListBoxAddButton}`} type="button" onClick={() => setFormData((prevData: any) => ({ ...prevData, value: [...prevData.value, ''] }))} >Add Content</button>
            {Array.isArray(formData.value) && formData.value.map((value: string, index: number) => (
              <div key={index}>
                <RowForm>
                  <input className={styles.nomodalInput} type="text" name={`value[${index}]`} value={JSON.stringify(value)} onChange={handleChange} />
                  <button className={`${styles.statesListBoxButton} ${styles.statesListBoxDeleteButton}`} type="button" onClick={() => setFormData((prevData: any) => ({ ...prevData, value: prevData.value.filter((_: any, i: number) => i !== index) }))} >Delete</button>
                </RowForm>
              </div>
            ))}
          </div>
        </RowForm>
        {error && <p className={styles.error}>{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Submit'}
        </button>
      </form>
    </div>
  )
}

export default ContentForm;
