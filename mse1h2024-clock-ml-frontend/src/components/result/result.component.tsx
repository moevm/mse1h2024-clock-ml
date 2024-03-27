import { FC } from "react";
import { Link } from "../link/link.component";

import css from "./result.module.css";
import { useAtomValue } from "jotai";
import { imgAtom } from "../../atoms/image";

interface IResultProps {
	score: number | null;
}

export const Result: FC<IResultProps> = ({ score }) => {
	const image = useAtomValue(imgAtom);

	const revokeLink = () => {
		image && URL.revokeObjectURL(image);
	};

	return (
		<section className={css.result}>
			<h1>Ваш результат</h1>
			<img src={image || ""} className={css.result__img} alt="Картинка результата" />
			<p>{score || 0}/10 баллов</p>
			<Link to="/" onClick={revokeLink}>
				Пройти заново
			</Link>
		</section>
	);
};
