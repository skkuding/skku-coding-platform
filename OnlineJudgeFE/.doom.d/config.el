;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom

;; sync' after modifying this file!

;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets.
(setq user-full-name "John Doe"
      user-mail-address "john@doe.com")

;; Doom exposes five (optional) variables for controlling fonts in Doom. Here
;; are the three important ones:
;;
;; + `doom-font'
;; + `doom-variable-pitch-font'
;; + `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;;
;; They all accept either a font-spec, font string ("Input Mono-12"), or xlfd
;; font string. You generally only need these two:
;; (setq doom-font (font-spec :family "monospace" :size 12 :weight 'semi-light)
;;       doom-variable-pitch-font (font-spec :family "sans" :size 13))

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
;; (setq doom-theme 'doom-one)
(setq doom-theme 'solarized-dark)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type nil)


;; Here are some additional functions/macros that could help you configure Doom:
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.

(use-package! term-keys)
(use-package! telega)
(after! vterm (term-keys-mode t))

(map! :map ivy-minibuffer-map
      "C-h" #'ivy-backward-delete-char)

(setq doom-font (font-spec :family "monaco" :size 16))
(setq confirm-kill-emacs nil)
;; (after! lsp-mode
;;   (lsp-register-client (make-lsp-client :new-connection (lsp-tramp-connection "pyls")
;;                                         :major-modes '(python-mode)
;;                                         :remote? t
;;                                         :server-id 'pyls-remote)))
(after! lsp-mode
  (lsp-register-client
   (make-lsp-client :new-connection (lsp-tramp-connection
                                     (lambda () lsp-clients-python-command))
                    :major-modes '(python-mode cython-mode)
                    :remote? t
                    :priority -1
                    :server-id 'pyls-remote
                    :library-folders-fn (lambda (_workspace) lsp-clients-python-library-directories)
                    :initialized-fn (lambda (workspace)
                                      (with-lsp-workspace workspace
                                        (lsp--set-configuration (lsp-configuration-section "pyls")))))))

(after! lsp-mode
  (lsp-register-client
   (make-lsp-client
    :new-connection (lsp-tramp-connection (lambda () (cons ccls-executable ccls-args)))
    :major-modes '(c-mode c++-mode cuda-mode objc-mode)
    :remote? t
    :server-id 'ccls-remote
    :multi-root nil
    :notification-handlers
    (lsp-ht ("$ccls/publishSkippedRanges" #'ccls--publish-skipped-ranges)
            ("$ccls/publishSemanticHighlight" #'ccls--publish-semantic-highlight))
    :initialization-options (lambda () ccls-initialization-options)
    :library-folders-fn ccls-library-folders-fn))
  )

(map! :map general-override-mode-map
      :ni "C-h" #'evil-window-left
      :ni "C-j" #'evil-window-down
      :ni "C-k" #'evil-window-up
      :ni "C-l" #'evil-window-right
      )


(map! (:when (featurep! :tools lookup)
       :nv "gr" #'+lookup/references)
       (:when (featurep! :tools eval)
        :nv "ger" #'+eval:region
        :n  "geR" #'+eval/buffer))

(custom-set-variables `(evil-disable-insert-state-bindings t))
(add-to-list 'default-frame-alist '(inhibit-double-buffering . t))

(setq projectile-require-project-root t)
(setq lsp-auto-guess-root t)
(setq-default lsp-file-watch-threshold 1000000)

(defun copy-with-osc52 (text &optional push)
  (send-string-to-terminal
   (concat "\ePtmux;\e\e]52;c;"
           (base64-encode-string (encode-coding-string text 'binary)
                                 t)
           "\a\e\\")))
(setq interprogram-cut-function `copy-with-osc52)

(set-language-environment "korean")
(prefer-coding-system `utf-8)
(global-set-key (kbd "§") 'toggle-input-method)


(map! (:when (featurep! :ui workspaces)
        "<f1>" #'+workspace/switch-to-0
        "<f2>" #'+workspace/switch-to-1
        "<f3>" #'+workspace/switch-to-2
        "<f4>" #'+workspace/switch-to-3
       ))

(map! :after vterm
      :map vterm-mode-map
      :ni "<f1>" #'+workspace/switch-to-0
      :ni "<f2>" #'+workspace/switch-to-1
      :ni "<f3>" #'+workspace/switch-to-2
      :ni "<f4>" #'+workspace/switch-to-3
      )
