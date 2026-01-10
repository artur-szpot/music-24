export interface MinionListQuery {
  episodes?: number[];
  ids?: number[];
  scenes?: number[];
  cards?: number[];
  rel?: string;
  view?: string;
}

export interface MinionListOwnProps {
  query: MinionListQuery;
}