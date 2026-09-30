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

export interface CategoryProps
  extends Interactive,
    CategoryOwnProps,
    CategoryActionProps {
  expanded?: boolean;
  topCategory?: boolean;
  onToggle: (id: number, isExpanded: boolean) => void;
  handleChosenCategory: (id: number) => void;
}

export const Category: React.FC<CategoryProps> = ({
  id,
  name,
  total,
  expanded,
  actions: actionsProps = [],
  navActions: navActionsProps = [],
  handleNav,
  subs,
  searchTerm,
  topCategory,
  globalLabels,
  chosenCategories: chosenCategoriesProps = {},
  openCategories: openCategoriesProps = [],
  onToggle,
  handleChosenCategory,
}: CategoryProps) => {
  const chosen = chosenCategoriesProps[id];
  const passableProps = {
    searchTerm,
    handleNav,
    globalLabels,
    handleChosenCategory,
    actions: actionsProps,
    navActions: navActionsProps,
  };
  const actionProps = { id, name, total };

  const [openSub, setOpenSub] = useState<number | undefined>(
    openCategoriesProps.find((openId) =>
      subs.map((sub) => sub.id).includes(openId),
    ),
  );
  // Each level owns which of its own subs is open, so opening one closes its siblings.
  const handleSubToggle = (subId: number, isExpanded: boolean) =>
    setOpenSub(isExpanded ? subId : undefined);
  const handleChosen = (chosenId: number) => () =>
    handleChosenCategory(chosenId);

  const actions = actionsProps.filter(
    ({ excludeTopCategories }) => !topCategory || !excludeTopCategories,
  );
  const navActions = navActionsProps.filter(
    ({ excludeTopCategories }) => !topCategory || !excludeTopCategories,
  );
  const hasSubs = subs.length > 0;

  return (
    <Accordion
      disableGutters
      key={name}
      expanded={hasSubs && Boolean(expanded)}
      onChange={(event, isExpanded) => hasSubs && onToggle(id, isExpanded)}
    >
      <AccordionSummary
        expandIcon={hasSubs && !searchTerm ? <ExpandMoreIcon /> : undefined}
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
            {chosen === true && <CheckBoxIcon onClick={handleChosen(id)} />}
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
                onClick={() => action.action(actionProps)}
              >
                {action.text(actionProps)}
              </span>
              {index !== actions.length - 1 ||
                (navActions.length > 0 && (
                  <span className="accordion-header separator">●</span>
                ))}
            </>
          ))}
          {navActions.map((action, index) => (
            <>
              <span
                className={`accordion-header action ${action.disabled && 'disabled'}`}
                onClick={() => handleNav.setScreen(action.action(actionProps))}
              >
                {action.text(actionProps)}
              </span>
              {index !== navActions.length - 1 && (
                <span className="accordion-header separator">●</span>
              )}
            </>
          ))}
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        {hasSubs && (
          <div className="accordion-box">
            {subs
              .filter((sub) => satisfiesSearchTerm(sub, searchTerm))
              .map((sub) => (
                <Category
                  {...sub}
                  {...passableProps}
                  expanded={searchTerm ? true : sub.id === openSub}
                  onToggle={handleSubToggle}
                  key={sub.id}
                />
              ))}
          </div>
        )}
      </AccordionDetails>
    </Accordion>
  );
};
