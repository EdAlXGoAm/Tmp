import styles from '../styles/utils/formatUtils.module.css';
import { CustomEdit } from './buttonUtils';

export const Row = ({ children, mt, mb, style }: { children: React.ReactNode, mt?: number, mb?: number, style?: React.CSSProperties }) => (
  <div className={`row mt-${mt ?? 1} mb-${mb ?? 2}`} style={style}>
    {children}
  </div>
);

export const Column = ({ children, width, mt, mb }: { children: React.ReactNode, width?: number, mt?: number, mb?: number }) => (
  <div className={`col-${width ?? 12} mt-${mt ?? 0} mb-${mb ?? 0}`}>
    {children}
  </div>
);

export const CustomForm = ({ children }: { children: React.ReactNode }) => {
  return (
    <form style={{ width: '100%' }}>
      {children}
    </form>
  )
}

export const RowForm = ({ children }: { children: React.ReactNode }) => {
  return (
    <Row mb={0} mt={0}>
      <Column>{children}</Column>
    </Row>
  )
}

export const ColumnTextCentered = ({ children, mt, mb }: { children: React.ReactNode, width?: number, mt?: number, mb?: number }) => (
  <div className={`col-12 mt-${mt ?? 0} mb-${mb ?? 0} text-center`}>
    {children}
  </div>
);


export const CenteredColumn = ({ children, width, mt }: { children: React.ReactNode, width?: number, mt?: number }) => (
  <div className={`row mt-${mt ?? 3} justify-content-center`}>
    <div className={`col-12 col-md-${width ?? 6}`}>
      {children}
    </div>
  </div>
);

export const Titles = ({ children, mt }: { children: React.ReactNode, mt?: number }) => (
  <div className={`row mt-${mt ?? 3}`}>
    <div className="col-12">
      {children}
    </div>
  </div>
);

export const Subtitle = ({ children, mt }: { children: React.ReactNode, mt?: number }) => (
  <div className={`row mt-${mt ?? 3}`}>
    <div className="col-12">
      <h4 className="Subtitle_Input">{children}</h4>
    </div>
  </div>
);

export const MiddleColumn = ({ children, width, mt }: { children: React.ReactNode, width?: number, mt?: number }) => (
  <div className={`col-${width ?? 6} mt-${mt ?? 3}`}>
    {children}
  </div>
);

export const MainJsonKey = ({ children}: { children: React.ReactNode }) => (
  <Row>
    <Column mt={0} mb={0}>
      <h4 style={{
        color: 'white',
        // backgroundColor Green
        backgroundColor: '#4CAF50',
        padding: '5px',
        paddingLeft: '15px',
        borderRadius: '5px',
      }}>{children}</h4>
    </Column>
  </Row>
);

export const JsonKeyGroup = ({ children, icon }: { children: React.ReactNode, icon: React.ReactNode }) => (
  <Row mt={0} mb={0}>
    <Column mb={1}>
      <span style={{
        fontSize: '0.7rem',
        color: 'white',
        // backgroundColor Green darken-4
        backgroundColor: '#1B5E20',
        padding: '5px',
        margin: '0px',
        borderRadius: '2px',
        display: 'inline-flex',
        alignItems: 'center',
        }}>
          {icon}&nbsp;
          {children}
        </span>
    </Column>
  </Row>
);

export const JsonKey = ({ children, icon, onClick }: { children: React.ReactNode, icon?: React.ReactNode, onClick?: () => void }) => (
  <Row mt={0} mb={0}>
    <Column mb={1}>
      <span
        onClick={onClick}
        style={{
          cursor: onClick ? 'pointer' : 'default',
          userSelect: onClick ? 'none' : 'auto',
          fontSize: '0.7rem',
          color: 'white',
          // backgroundColor Green darken-4
          backgroundColor: '#81C784',
          padding: '5px',
          margin: '0px',
          borderRadius: '2px',
          display: 'inline-flex',
          alignItems: 'center',
        }}>
          {icon && <>{icon}&nbsp;</>}
          {children}
        </span>
    </Column>
  </Row>
);

export const JsonValue = ({ children }: { children: React.ReactNode }) => (
  <pre style={{
    fontSize: '0.7rem',
    color: 'black',
    // backgroundColor Green lighten-3
    backgroundColor: '#C8E6C9',
    padding: '5px',
    margin: '0px',
    borderRadius: '2px',
    display: 'inline-block'
  }}>{children}</pre>
);

export const CardContainer = ({ children }: { children: React.ReactNode }) => (
  <div className="row">
    <div className="col-12">
      <div className="card card-body"
        style={{padding: '6px'}}
        >
        {children}
      </div>
    </div>
  </div>
);

export const VariableText = ({ variable, value, onClick }: { variable: String, value: String, onClick: () => void}) => {
  return (
    <>
      <span className={styles.paddingSpanText}>
        <span className={styles.textSmallBold}>
          {`${variable}: `}
        </span>
        <span className={styles.textSmall}>
          {value !== '' ? (
          `${value} `
          ) : (
            <span style={{
              color: '#596f75',
              fontStyle: 'italic'
            }}>
            {`empty `}
            </span>
          )}
        </span>
        <span>
          <CustomEdit onClick={onClick}/>
        </span>
      </span>
    </>
  )
}

export const VariableTextBorder = ({ variable, value, color, onClick }: { variable: String, value: String, color: String, onClick: () => void }) => {
  return (
    <>
      <span className={styles.paddingSpanText}>
        <span className={styles.textSmallBold}>
          {`${variable}: `}
        </span>
        <span className={styles.textSmall}
        style={{
          padding: '2px',
          border: value !== '' ? `3px solid ${color ? color : '#ddd'}` : '',
          borderRadius: '5px'
        }}>
          {value !== '' ? (
          `${value} `
          ) : (
            <span style={{
              color: '#596f75',
              fontStyle: 'italic'
            }}>
            {`empty `}
            </span>
          )}
        </span>
        <span>
          <CustomEdit onClick={onClick}/>
        </span>
      </span>
    </>
  )
}

export const SimpleCodeContainer = ({ code, color }: { code: String, color?: String }) => {
  return (
    <div style={{ position: 'relative', border: `${color ? '3' : '1'}px solid ${color ? color : '#ddd'}`, borderRadius: '5px', paddingLeft: '10px', padding: '2px', backgroundColor: '#f5f5f5' }}>
      <pre style={{ margin: 0 }}>
        <code>{code}</code>
      </pre>
    </div>
  )
}

export const VariableArray = ({ variable, value, color, onClick }: { variable: String, value: Object, color: String, onClick: () => void }) => {
  return (
    <>
      <span className={styles.paddingSpanText}>
        <span className={styles.textSmallBold}>
          {`${variable}: `}
        </span>
        {Array.isArray(value) && value.length > 0 ?
          <>
            <span>
              <CustomEdit onClick={onClick}/>
            </span>
            <div style={{paddingLeft: '15px'}}>
              <CardContainer>
                {value.map((element, i) => (
                  <div key={i}>
                    <SimpleCodeContainer code={JSON.stringify(element)} color={color}/>
                  </div>
                ))}
              </CardContainer>
            </div>
          </>
         : (
          <>
            <span className={styles.textSmall} style={{
              color: '#596f75',
              fontStyle: 'italic'
            }}>
            {`empty `}
            </span>
            <span>
              <CustomEdit onClick={onClick}/>
            </span>
          </>
        )}
      </span>
    </>
  )
}

export const VariableArrayMinimalist = ({ variable, value, onClick }: { variable: String, value: Object, onClick: () => void }) => {
  return (
    <>
      <span className={styles.paddingSpanText}>
        <span className={styles.textSmallBold}>
          {`${variable}: `}
        </span>
        {Array.isArray(value) && value.length > 0 ?
          <>
            <span>
              <CustomEdit onClick={onClick}/>
            </span>
            <div style={{paddingLeft: '15px'}}>
              <CardContainer>
                <SimpleCodeContainer code={JSON.stringify(value)}/>
              </CardContainer>
            </div>
          </>
         : (
          <>
            <span className={styles.textSmall} style={{
              color: '#596f75',
              fontStyle: 'italic'
            }}>
            {`empty `}
            </span>
            <span>
              <CustomEdit onClick={onClick}/>
            </span>
          </>
        )}
      </span>
    </>
  )
}

export const MiniTitle = ({ title }: { title: String}) => {
  return (
    <>
      <Row mt={0} mb={0}>
        <ColumnTextCentered>
          <span className={styles.textSmallBold}>{title}</span>
        </ColumnTextCentered>
      </Row>
    </>
  )
}
