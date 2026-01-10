export interface CardProps {
   id: number;
   name: string;
   category: string;
   cardType: string;
   parent?: number | null;
   view: string | null;
 }