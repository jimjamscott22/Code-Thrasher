import Editor, { type Monaco } from "@monaco-editor/react";

function defineTheme(monaco: Monaco) {
  monaco.editor.defineTheme("code-thrasher-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [],
    colors: {
      "editorCursor.foreground": "#FFFFFF",
      "editorCursor.background": "#000000",
      "editorForeground": "#C5C5C5",
      "editorBackground": "#1E1E1E",
      "editorLineNumberForeground": "#6A9955",
      "editorLineNumberBackground": "#1E1E1E",
      "selectionBackground": "#264F78",
      "keywordInfo": "#CE9178",
      "functionInfo": "#4EC9B0",
      "stringInfo": "#CE9178",
      "commentInfo": "#5C6370",
    },
  });
}

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  height?: string;
  readOnly?: boolean;
}

export default function CodeEditor({
  value,
  onChange,
  height = "400px",
  readOnly = false,
}: CodeEditorProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-gray-700 bg-gray-950">
      <div className="flex items-center gap-2 border-b border-gray-700 bg-gray-900 px-3 py-2">
        <span className="h-3 w-3 rounded-full bg-red-500" />
        <span className="h-3 w-3 rounded-full bg-yellow-500" />
        <span className="h-3 w-3 rounded-full bg-green-500" />
        <span className="ml-2 font-mono text-xs text-gray-500">solution.py</span>
      </div>
      <Editor
        height={height}
        defaultLanguage="python"
        theme="code-thrasher-dark"
        beforeMount={defineTheme}
        value={value}
        onChange={(v) => onChange(v ?? "")}
        options={{
          fontSize: 14,
          fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
          fontLigatures: true,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          readOnly,
          padding: { top: 12, bottom: 12 },
          renderLineHighlight: "gutter",
          lineNumbers: "on",
        }}
      />
    </div>
  );
}
