import { DB_OPERATIONS } from '../../enums/db';
import { SCREEN_TYPES } from '../../enums/screens';
import { CategoryOwnProps } from '../components/CategoryProps';
import { CardDetailsOwnProps } from '../screens/CardDetailsProps';
import { CategoryListOwnProps } from '../screens/CategoryListProps';
import { MinionDetailsOwnProps } from '../screens/MinionDetailsProps';
import { MinionListOwnProps, MinionListQuery } from '../screens/MinionListProps';

export interface SetScreenProps {
cardDetails?: CardDetailsOwnProps
categoryList?: CategoryListOwnProps
minionDetails?: MinionDetailsOwnProps
minionList?: MinionListOwnProps
  popup?: SetScreenProps;
  screenType: SCREEN_TYPES
}

interface NavToCommon {
   screenType?: SCREEN_TYPES
}

interface NavTo {
   cardDetails: (args:{id:number}&NavToCommon) => SetScreenProps
tagsList: (args:{searchTerm?:string}&NavToCommon)=> SetScreenProps
   cardImplementationsList: (args:{searchTerm?:string}&NavToCommon)=> SetScreenProps
   scenesList: (args:{searchTerm?:string}&NavToCommon)=> SetScreenProps
minionDetails: (args: {id:number} & NavToCommon)=> SetScreenProps
minionList: (args:{query: MinionListQuery}&NavToCommon)=> SetScreenProps
}

export const navTo: NavTo = {
   cardDetails: ({id,screenType}) => ({
      cardDetails:{id},
      screenType:screenType??SCREEN_TYPES.SCREEN
   }),
   tagsList: ({            searchTerm,  screenType}) => ({
      categoryList:{
         dbOperation: DB_OPERATIONS.GET_TAG_CATEGORIES,
         searchTerm,
         navActions: [
           {
             excludeTopCategories: true,
             text: (props: CategoryOwnProps) => `View ${props.total} images`,
             navAction: (props: CategoryOwnProps) => navTo.minionList({query: {
               cards: [props.id!],
               rel: 'p',
             }})
           },
           { text: () => 'Edit subs', action: () => null, disabled: true },
         ],     
      },
      screenType:screenType??SCREEN_TYPES.SCREEN
   }),
   cardImplementationsList: ({            searchTerm,  screenType}) => ({
      categoryList:{
         dbOperation: DB_OPERATIONS.GET_IMPLEMENTATION_CATEGORIES,
         searchTerm,
         actions: [         ],     
      },
      screenType:screenType??SCREEN_TYPES.SCREEN
   }),
   scenesList: ({            searchTerm,  screenType}) => ({
      categoryList:{
         dbOperation: DB_OPERATIONS.GET_SCENES,
         searchTerm,
         actions: [
            {
              excludeTopCategories: true,
              text: (props: CategoryOwnProps) => `View ${props.total} images`,
              navAction: (props: CategoryOwnProps) => navTo.minionList({query: {
               ...(props.id! < 0 && { episodes: [-props.id!] }),
               ...(props.id! >= 0 && { scenes: [props.id!] }),
              }})
            },
          ],
      },
      screenType:screenType??SCREEN_TYPES.SCREEN
   }),
   minionDetails: ({id, screenType}) => ({
      minionDetails:{id},
      screenType:screenType??SCREEN_TYPES.SCREEN
   }),
   minionList: ({query,screenType}) => ({
      minionList:{query},
      screenType:screenType??SCREEN_TYPES.SCREEN
   })
}