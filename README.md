# Food Product Cards

把完整立项、产品实物图、卖点与策略，变成统一风格的食品产品卡和菜单。

默认保留深棕 × 奶油色、Peet’s Logo、菜单加价分组，以及「实物图 / 拆层图 / 卖点·风味口感·策略」版式。食品默认拆层。饮品采用同杯中线分割：左半真实照片、右半连续分层剖面，右侧引线解读。食品保留悬浮拆层；饮品层次留在杯内。

## 安装到 Codex

```sh
git clone https://github.com/louiseboo/food-product-cards.git
mkdir -p ~/.codex/skills
cp -R food-product-cards/skills/food-product-cards ~/.codex/skills/
```

重新打开会话，调用 `$food-product-cards`，提供完整立项、原图、卖点和策略。先确认文字，再制作。已有同名安装时，请先备份旧目录。

## 运行示例

```sh
python3 skills/food-product-cards/scripts/render.py examples/demo.json demo.html
python3 -m unittest discover -s tests -v
```

Python 3.9+，渲染器无第三方依赖。打开 HTML 可离线查看；浏览器打印时开启背景并使用 CSS 页面尺寸。真实拆层图需要所在 Agent 环境提供图像生成能力，渲染器本身不生成图片。

饮品制作规则见 `skills/food-product-cards/references/beverages.md`。需提供真实原图和确认过的层次信息；渲染器不会自动把原图变成剖面。

公开示例使用虚构文字和抽象示意资产，仅展示布局，不代表真实在售产品。没有业务原稿、内部经营数据或未上市产品图片。Peet’s 名称与 Logo 属于其权利人；本项目不是官方产品，不授予商标权。用户可替换品牌资产。

## 文件

- `skills/food-product-cards/SKILL.md`：Agent 工作规则。
- `scripts/render.py`：嵌入图片并生成 HTML。
- `references/`：输入格式与拆层规则。
- `examples/`：可运行的虚构案例。

验证边界：自动测试检查输入拒绝、HTML 转义、离线图片和菜单排序；实际生成的拆层是否准确、策略是否完整仍需对照原始材料目视验收。
