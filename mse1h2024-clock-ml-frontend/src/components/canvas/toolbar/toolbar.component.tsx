import { useState, MouseEvent, FC, ChangeEvent } from "react";
import css from "./toolbar.module.css";

import clx from "classnames";
import { TToolbar, TTools } from "../../../types";

type TPropsToolbar = {
	onSelect?: (value: TToolbar) => any;
};

export const Toolbar: FC<TPropsToolbar> = ({ onSelect }) => {
	const [tool, setTool] = useState<TTools>("brush");
	const [size, setSize] = useState(2);

	function onSelectHandler(ev: MouseEvent<HTMLElement>) {
		const target = (ev.target as HTMLElement).closest("[data-value]") as HTMLElement;
		const value = target?.dataset?.value! as TTools | "size";

		if (value === "size" || !value) return;
		setTool(value);
		onSelect?.({
			tool: value,
			size,
		});
	}

	function onSetSize(e: ChangeEvent<HTMLInputElement>) {
		setSize(+e.target.value);
		onSelect?.({
			tool,
			size: +e.target.value,
		});
	}

	return (
		<ul className={css.toolbar} onClick={onSelectHandler}>
			<li data-value="eraser" className={clx({ [css.active]: tool === "eraser" })}>
				<img src="./eraser.svg" alt="Резинка" />
			</li>
			<li data-value="brush" className={clx({ [css.active]: tool === "brush" })}>
				<img src="./brush.svg" alt="Кисточка" />
			</li>
			<li data-size={size} className={css["size-selector"]}>
				<label>
					<span>{size}</span>
					<input type="range" value={size} onChange={onSetSize} step={1} min={1} max={50} />
				</label>
			</li>
		</ul>
	);
};
