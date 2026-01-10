import CheckBoxIcon from '@mui/icons-material/CheckBox';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Icon from '@mui/material/Icon';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import { Interactive } from '../interfaces/interactive';
import { CategoryActionProps } from './CategoryActionProps';
import { CategoryOwnProps, satisfiesSearchTerm } from './CategoryProps';

export interface CategoryProps extends Interactive, CategoryOwnProps, CategoryActionProps {
  expanded?: boolean;
  topCategory?: boolean;
  handleOpenCategory: (args:{add?:number|undefined, remove?:number|undefined}) => void;
  handleChosenCategory:     (id: number) =>void
}

export const Category: React.FC<CategoryProps> = ({id,name,expanded,actions:actionsProps,navActions:navActionsProps,handleNav, subs, searchTerm, topCategory, globalLabels, chosenCategories:chosenCategoriesProps={}, openCategories: openCategoriesProps=[], handleOpenCategory ,handleChosenCategory }: CategoryProps) => {
const chosen = chosenCategoriesProps[id]
const passableProps = {
   searchTerm,
   handleNav,
   globalLabels,
   handleOpenCategory,
   handleChosenCategory,
   actions:actionsProps,
   navActions:navActionsProps}

  const [openSub, setOpenSub] = useState<string | undefined>(openCategoriesProps.find((id)=>subs.map((sub)=>sub.id).includes(id)));
  const handleOpenSub =
    (id: number) =>
    (event: React.SyntheticEvent, newExpanded: boolean) => {
       newExpanded ? handleOpenCategory({add:id, remove: openSub}) : handleOpenCategory({remove:openSub})
       setOpenSub(newExpanded ? id : undefined);
    }; 
     const handleChosen =
    (id: number) =>
    (event: React.SyntheticEvent) => handleChosenCategory(id)

  const actions = actionsProps.filter(
    ({ excludeTopCategories }) => !topCategory || !excludeTopCategories,
  );
  const navActions = navActionsProps.filter(
    ({ excludeTopCategories }) => !topCategory || !excludeTopCategories,
  );

  return (
    <Accordion
      disableGutters
      key={name}
      expanded={expanded}
      onChange={handleOpenSub(id)}
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
              <HighlightOffIcon onClick={handleChosen(id)} />
            )}
            {chosen === true && (
              <CheckBoxIcon onClick={handleChosen(id)} />
            )}
            {chosen === undefined && (
              <CheckBoxOutlineBlankIcon onClick={handleChosen(id)} />
            )}
          </Icon>
        )}
        <Typography>
          <span className="accordion-main-header">{name}</span>
          {actions.map((action, index) => (
            <>
              <span
                className={`accordion-header action ${action.disabled && 'disabled'}`}
                onClick={() => action.action(props)}
              >
                {action.text(props)}
              </span>
              {index !== actions.length - 1 && navActions.length === 0 && (
                <span className="accordion-header separator">●</span>
              )}
            </>
          ))}
          {navActions.map((action, index) => (
            <>
              <span
                className={`accordion-header action ${action.disabled && 'disabled'}`}
                onClick={() => handleNav.setScreen( action.action(props))}
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
                  {...passableProps}
                  expanded={searchTerm ? true : sub.id === openSub}
                  key={sub.id}
                />
              ))}
          </div>
        )}
      </AccordionDetails>
    </Accordion>
  );
};
