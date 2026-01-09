import CheckBoxIcon from '@mui/icons-material/CheckBox';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Icon from '@mui/material/Icon';
import Typography from '@mui/material/Typography';
import { useEffect, useState } from 'react';
import { Interactive } from './interactive';

export interface CategoryOwnProps {
  category?: string;
  id: number | null;
  name?: string;
  total?: number;
  subs: CategoryOwnProps[];
  searchTerm?: string;
  chosen?: boolean;
}

export interface CategoryAction {
  excludeTopCategories?: boolean;
  text: (props: CategoryOwnProps) => string;
  action: (props: CategoryOwnProps) => void;
  disabled?: boolean;
}

export interface CategoryProps extends Interactive, CategoryOwnProps {
  expanded?: boolean;
  onChange: (event: React.SyntheticEvent, newExpanded: boolean) => void;
  actions: CategoryAction[];
  topCategory?: boolean;
}

export const satisfiesSearchTerm: (
  category: CategoryOwnProps,
  searchTerm?: string,
) => boolean = (category: CategoryOwnProps, searchTerm?: string) => {
  if (!searchTerm) {
    return true;
  }
  if (category.name?.toLowerCase().includes(searchTerm)) {
    return true;
  }
  return category.subs.some((sub) => satisfiesSearchTerm(sub, searchTerm));
};

export const Category: React.FC<CategoryProps> = (props: CategoryProps) => {
  const { handleNav, subs, searchTerm, topCategory, globalLabels } = props;
  const [openSub, setOpenSub] = useState<string | undefined>(undefined);
  const handleOpenSub =
    (category: string) =>
    (event: React.SyntheticEvent, newExpanded: boolean) => {
      setOpenSub(newExpanded ? category : undefined);
    };

  const [chosen, setChosen] = useState<boolean | undefined>(undefined);
  useEffect(() => {
    setChosen(props.chosen);
  }, [props.chosen]);

  const handleToggleChosen = () => {
    switch (chosen) {
      case undefined:
        setChosen(true);
        break;
      case true:
        setChosen(false);
        break;
      case false:
        setChosen(undefined);
        break;
    }
  };

  const actions = props.actions.filter(
    ({ excludeTopCategories }) => !topCategory || !excludeTopCategories,
  );

  return (
    <Accordion
      disableGutters
      key={props.name}
      expanded={props.expanded}
      onChange={props.onChange}
    >
      <AccordionSummary
        expandIcon={searchTerm ? undefined : <ExpandMoreIcon />}
      >
        {!topCategory && searchTerm && (
          <Icon
            className="category-icon"
            color={
              chosen === undefined ? 'primary' : chosen ? 'success' : 'error'
            }
          >
            {chosen === false && (
              <HighlightOffIcon onClick={() => handleToggleChosen()} />
            )}
            {chosen === true && (
              <CheckBoxIcon onClick={() => handleToggleChosen()} />
            )}
            {chosen === undefined && (
              <CheckBoxOutlineBlankIcon onClick={() => handleToggleChosen()} />
            )}
          </Icon>
        )}
        <Typography>
          <span className="accordion-main-header">{props.name}</span>
          {actions.map((action, index) => (
            <>
              <span
                className={`accordion-header action ${action.disabled && 'disabled'}`}
                onClick={() => action.action(props)}
              >
                {action.text(props)}
              </span>
              {index !== actions.length - 1 && (
                <span className="accordion-header separator">●</span>
              )}
            </>
          ))}
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        {subs.length > 0 && (
          <div className="accordion-box">
            {subs
              .filter((sub) => satisfiesSearchTerm(sub, searchTerm))
              .map((sub) => (
                <Category
                  {...sub}
                  searchTerm={searchTerm}
                  key={sub.name}
                  handleNav={handleNav}
                  globalLabels={globalLabels}
                  expanded={searchTerm ? true : sub.name === openSub}
                  onChange={handleOpenSub(sub.name ?? '')}
                  actions={props.actions}
                />
              ))}
          </div>
        )}
      </AccordionDetails>
    </Accordion>
  );
};
