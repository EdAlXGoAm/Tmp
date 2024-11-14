import styles from '../styles/utils/buttonUtils.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faAngleDown, faAngleLeft, faAngleRight, faClipboard, faEdit, faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import { Button } from '@mui/material';

export const LeftAngle = () => {
  return <FontAwesomeIcon icon={faAngleLeft} className={styles.leftAngle} />;
};

export const RightAngle = () => {
  return <FontAwesomeIcon icon={faAngleRight} className={styles.rightAngle} />;
};

export const CustomClipboardButton = ({ onClick, copied }: { onClick: () => void, copied: boolean }) => {
  return (
    <div className={styles.faContainerTopRight}>
      <div className={styles.faButtons} onClick={onClick}
        style={{color: copied ? 'green' : '#212529'}}>
        <FontAwesomeIcon icon={faClipboard} size="sm" />
      </div>
    </div>
  )
};

export const CustomAngleRight = () => {
  return (
    <div>
      <div className={styles.faButtons}>
        <FontAwesomeIcon icon={faAngleRight} size="sm" />
      </div>
    </div>
  )
}

export const CustomAngleDown = () => {
  return (
    <div>
      <div className={styles.faButtons}>
        <FontAwesomeIcon icon={faAngleDown} size="sm" />
      </div>
    </div>
  )
}

export const CustomEdit = ({ onClick }: { onClick: () => void }) => {
  return (
    <span className={styles.faButtons} onClick={onClick}>
      <FontAwesomeIcon icon={faEdit} size="sm" />
    </span>
  )
}

export const CustomDelete = ({ onClick, deleteable }: { onClick: () => void, deleteable: boolean }) => {
  return (
    <div className={styles.faContainerTopRight}>
      <span className={styles.faButtons} onClick={onClick}
        style={{color: deleteable ? '#dc3545' : '#212529'}}>
        <FontAwesomeIcon icon={faTrash} size="sm" />
      </span>
    </div>
  )
}

export const CustomAddHere = ({ onClick, addable }: { onClick: () => void, addable: boolean }) => {
  return (
    <span className={styles.faButtons} onClick={onClick}
      style={{color: addable ? '#4CAF50' : '#212529'}}>
      <FontAwesomeIcon icon={faPlus} size="sm" />
    </span>
  )
}

export const MiniFloatingButton = ({ onClick, boolean_var, text1, text2 }: { onClick: () => void, boolean_var: boolean, text1: string, text2: string }) => {
  return (
    <Button
      onClick={onClick}
      size="small"
      style={{
        position: 'absolute',
        left: '20px',
        top: '5px',
        zIndex: 1000,
        padding: '0',
        margin: '0',
        fontSize: '10px'
      }}
    >
      {boolean_var ? text1 : text2}
    </Button>
  )
}

export const MiniTableButton = ({ onClick, boolean_var, text1, text2 }: { onClick: () => void, boolean_var: boolean, text1: string, text2: string }) => {
  return (
    <Button 
      onClick={onClick} 
      size="small"
      style={{
        padding: '0',
        margin: '0',
        fontSize: '10px',
        backgroundColor: boolean_var ? '#4CAF50' : '#212529',
        color: '#fff'
      }}
    >
      {boolean_var ? text1 : text2}
    </Button>
  )
}
