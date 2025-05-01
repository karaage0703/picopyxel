#!/bin/bash
# deploy.sh - Pyxelパッケージを作成し実機に転送するスクリプト

# デフォルト値
DEFAULT_PACKAGE_NAME="picopyxel"
DEFAULT_PYTHON_FILE="picopyxel/main.py"
DEFAULT_HOST="plumOS-RN"
DEFAULT_PASSWORD="plum"
DEFAULT_REMOTE_DIR="/storage/roms/pyxel"

# 引数の解析
PACKAGE_NAME=${1:-$DEFAULT_PACKAGE_NAME}
PYTHON_FILE=${2:-$DEFAULT_PYTHON_FILE}
HOST=${3:-$DEFAULT_HOST}
PASSWORD=${4:-$DEFAULT_PASSWORD}

# パッケージファイルのパス
PACKAGE_FILE="${PACKAGE_NAME}.pyxapp"

# 色付きの出力関数
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# 依存関係のチェック
check_dependencies() {
    print_info "依存関係をチェックしています..."

    # pyxelコマンドのチェック
    if ! command -v pyxel &> /dev/null; then
        print_error "pyxelコマンドが見つかりません。Pyxelがインストールされているか確認してください。"
        exit 1
    fi

    # sshpassコマンドのチェック
    if ! command -v sshpass &> /dev/null; then
        print_error "sshpassコマンドが見つかりません。インストールしてください。"
        print_info "Macの場合: brew install hudochenkov/sshpass/sshpass"
        print_info "Linuxの場合: sudo apt-get install sshpass"
        exit 1
    fi
}

# Pyxelパッケージの作成
create_package() {
    print_info "Pyxelパッケージを作成しています: ${PACKAGE_FILE}"

    if [ ! -f "$PYTHON_FILE" ]; then
        print_error "Pythonファイルが見つかりません: ${PYTHON_FILE}"
        exit 1
    fi

    pyxel package "$PACKAGE_NAME" "$PYTHON_FILE"

    if [ ! -f "$PACKAGE_FILE" ]; then
        print_error "パッケージの作成に失敗しました。"
        exit 1
    fi

    print_success "パッケージを作成しました: ${PACKAGE_FILE}"
}

# 実機へのパッケージ転送
transfer_to_device() {
    print_info "パッケージを実機に転送しています..."
    print_info "ホスト: ${HOST}"
    print_info "リモートディレクトリ: ${DEFAULT_REMOTE_DIR}"

    sshpass -p "$PASSWORD" sftp root@$HOST <<EOF
cd $DEFAULT_REMOTE_DIR
put $PACKAGE_FILE
EOF

    if [ $? -eq 0 ]; then
        print_success "パッケージを実機に転送しました。"
        print_info "実機の以下のパスにパッケージがあります: ${DEFAULT_REMOTE_DIR}/${PACKAGE_FILE}"
    else
        print_error "パッケージの転送に失敗しました。ネットワーク接続と認証情報を確認してください。"
        exit 1
    fi
}

# メイン処理
main() {
    print_info "PicoPixel実機デプロイツール"
    print_info "============================"

    check_dependencies
    create_package
    transfer_to_device

    print_success "デプロイが完了しました！"
    print_info "実機でPyxelランチャーを起動し、${PACKAGE_NAME}を選択して実行してください。"
}

# スクリプトの実行
main