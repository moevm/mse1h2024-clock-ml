import { FC, PropsWithChildren } from "react";
import css from "./layout.module.css";
import clx from "classnames";

export const Layout: FC<PropsWithChildren<{ linear?: boolean }>> = ({ children, linear }) => {
	return <main className={clx(css.layout, { [css.linear]: linear })}>{children}</main>;
};
