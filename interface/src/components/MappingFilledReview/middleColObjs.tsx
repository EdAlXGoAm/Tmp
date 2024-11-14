import { useState } from "react";
import { MainJsonKey } from "../../utils/formatUtils";
import { MiddleColumn } from "../../utils/formatUtils";
import styles from '../../styles/columnRelationship.module.css';
import { MiniFloatingButton } from "../../utils/buttonUtils";
import { JsonNestedTreeView } from "./jsonNestedTreeView";

interface MiddleColObjsProps {
  mainKey: string;
  value: any;
}

export const MiddleColObjs = ({ mainKey, value }: MiddleColObjsProps) => {
  const [expanded, setExpanded] = useState(true);
  const [forceInvisibility, setForceInvisibility] = useState(false);
  const [forceVisibility, setForceVisibility] = useState(false);

  const handleExpand = () => {
    setExpanded(!expanded);
    if (expanded) {
      setForceInvisibility(true);
    } else {
      setForceVisibility(true);
    }
  }

  return (
    <MiddleColumn>
      <MiniFloatingButton onClick={() => handleExpand()} boolean_var={expanded} text1={'Collapse All'} text2={'Expand All'} />
      <div className={styles.scrollableContainer} style={{marginTop: '20px'}}>
        <MainJsonKey>{mainKey}</MainJsonKey>
        {Object.entries(value).map(([key, value]: [string, any], i: number) => (
          <JsonNestedTreeView
            key={`${i}`}
          jsonPath={[key]}
          jsonKey={key}
          jsonValue={value}
          forceInvisibility={forceInvisibility}
          setForceInvisibility={setForceInvisibility}
          forceVisibility={forceVisibility}
          setForceVisibility={setForceVisibility}
          />
        ))}
      </div>
    </MiddleColumn>
  )
}

