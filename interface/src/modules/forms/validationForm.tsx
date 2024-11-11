import React, { useEffect } from 'react';
import styles from '../../styles/ValidationForm.module.css';
import { ValidationFormElements } from '../../constants/forms/validationFormElements';
import { Switch, FormControlLabel } from '@mui/material';
import { RowForm } from '../../utils/formatUtils';

interface ValidationFormProps {
  elementToEdit: any;
  onCleanData: () => void;
  isOpenExternal: boolean;
  setIsOpenExternal: React.Dispatch<React.SetStateAction<boolean>>;
  updateValidation: (key: string, value: string) => void;
  createValidation: (value: string) => void;
}

const ValidationForm: React.FC<ValidationFormProps> = ({
  elementToEdit,
  onCleanData,
  isOpenExternal,
  updateValidation,
  createValidation
}) => {
  const {
    isOpen, setIsOpen,
    error,
    loading,
    formData, setFormData,
    handleChange,
    handleChangeCheckbox,
    handleSubmit,
    handleClose
  } = ValidationFormElements({ onCleanData, elementToEdit, updateValidation, createValidation });

  useEffect(() => {
    if(elementToEdit) {
      if (Array.isArray(elementToEdit.value)) {
        setFormData((prevData: any) => ({ ...prevData, type: true, value: elementToEdit.value }));
      } else {
        setFormData((prevData: any) => ({ ...prevData, type: false, value: elementToEdit.value }));
      }
      setIsOpen(true);
    }
  }, [elementToEdit]);

  useEffect(() => {
    setIsOpen(isOpenExternal);
  }, [isOpenExternal]);

  useEffect(() => {
    if (formData.type) {
      if (typeof formData.value === 'string') {
        const newFormDataValueArray = formData.value.split(', ');
        if (newFormDataValueArray.length === 0) {  
          setFormData((prevData: any) => ({ ...prevData, value: [] }));
        } else {
          setFormData((prevData: any) => ({ ...prevData, value: newFormDataValueArray }));
        }
      }
    } else {
      if (Array.isArray(formData.value)) {
        if (formData.value.length === 0) {
          setFormData((prevData: any) => ({ ...prevData, value: '' }));
        } else {
          const newFormDataValueString = formData.value.join(', ');
          setFormData((prevData: any) => ({ ...prevData, value: newFormDataValueString }));
        }
      }
    }
  }, [formData.type]);

  return (
    <>
      {isOpen && (
        <div className={styles.overlay} onClick={handleClose}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h2>{elementToEdit ? 'Edit Validation' : 'Add Validation'}</h2>
            <form onSubmit={handleSubmit}>
              <RowForm>
                <label>Validation</label>
                <RowForm>
                  <FormControlLabel control={<Switch name="type" checked={formData.type} onChange={handleChangeCheckbox} />} label={`${formData.type ? 'Array' : 'String'}`} />
                </RowForm>
                {formData.type ? (
                  <div className={styles.statesListBox}>
                    <button className={`${styles.statesListBoxButton} ${styles.statesListBoxAddButton}`}
                      type="button"
                      onClick={() => setFormData((prevData: any) => ({ ...prevData, value: [...prevData.value, ''] }))}
                    >
                      Agregar Estado
                    </button>
                    {Array.isArray(formData.value) && formData.value.map((validation: string, index: number) => (
                      <div key={index}>
                        <RowForm>
                          <input className={styles.nomodalInput} type="text" name={`value[${index}]`} value={validation} onChange={handleChange} />
                        <button className={`${styles.statesListBoxButton} ${styles.statesListBoxDeleteButton}`}
                          type="button"
                          onClick={() => setFormData((prevData: any) => ({ ...prevData, value: prevData.value.filter((_: any, i: number) => i !== index) }))}
                            >
                              Eliminar
                            </button>
                          </RowForm>
                        </div>
                      ))}
                  </div>
                ) : (
                  <input type="text" name="value" value={formData.value} onChange={handleChange} />
                )}
              </RowForm>
              {error && <p className={styles.error}>{error}</p>}
              <button type="submit" disabled={loading}>
                {loading ? 'Loading...' : 'Submit'}
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default ValidationForm;
