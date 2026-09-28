export interface CardProps {
  id: number;
  name: string;
  category: string | null;
  cardType: string;
  parent?: number | null;
  view: string | null;
}
