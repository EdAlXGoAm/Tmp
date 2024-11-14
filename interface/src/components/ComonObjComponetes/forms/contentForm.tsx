import React, { useEffect } from 'react';
import styles from '../../../styles/forms/contentForm.module.css';
import { ContentFormElements } from '../../../constants/TestCasesMapping/forms/contentFormElements';
import { RowForm } from '../../../utils/formatUtils';

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
    setIsOpen,
    error,
    loading,
    formData, setFormData,
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
        <div className={styles.buttons}>
          <button type="submit" disabled={loading}>
            {loading ? 'Updating...' : (elementToEdit ? 'Update' : 'Add')}
          </button>
        </div>
      </form>
    </div>
  )
}

export default ContentForm;
