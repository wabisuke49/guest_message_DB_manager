---
name: git-make-pr
description: 変更履歴と関連Issueを確認し、日本語で構造化したGitHub Pull Requestを作成する。
---

# GitHub Pull Requestの作成

ブランチの変更とコミット履歴を分析し、レビューしやすいPull Requestを作成する。

## 内容のルール

- タイトルと本文は日本語で書く。
- タイトルはConventional Commitsの `<type>(<scope>): <description>` 形式にする。
- 本文には「概要」「関連Issue」「変更点」「動作確認」を含める。
- 「変更点」はコミット履歴をそのまま列挙せず、技術的に重要な変更を要約する。
- 関連Issueを必ず記載する。完了するIssueには `Closes #<number>` または `Fixes #<number>`、参照だけなら `Refs #<number>` を使う。

## 作成手順

1. 現在のブランチ、ベースブランチとの差分、コミット履歴、関連Issueを確認する。
2. タイトル、本文、ベースブランチ、ヘッドブランチをユーザーに提示して確認を得る。
3. 本文は安全な一時Markdownファイルに書き出し、`gh pr create --body-file <path>` でPRを作成する。必要に応じてベースとヘッドを明示する。
4. 作成後はPRのURLを報告し、一時ファイルを削除する。

## 境界

PR作成はリモートの状態を変更する操作であるため、必ずユーザー確認後に実行する。未解決の重大な差分やテスト失敗がある場合は、その内容を明示して判断を仰ぐ。
