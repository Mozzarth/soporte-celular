"""Cliente MCP mínimo para manejar la ventana de SolidCraft abierta con `solidcraft --control 7878`.

Uso:
  python3 live.py <herramienta> '<json args>'
  python3 live.py batch-file soporte.json      # reproduce un script en la ventana
"""
import json, subprocess, sys

PUERTO = 7878


def llamar(tool, args=None):
    return sesion([(tool, args or {})])[0]


def sesion(llamadas):
    """Varias llamadas en una sola conexión; se detiene en la primera que falle."""
    p = subprocess.Popen(['solidcraft-cli', 'mcp', '--connect', f'127.0.0.1:{PUERTO}', '--allow-any-path'],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    def enviar(msg):
        p.stdin.write(json.dumps(msg) + '\n')
        p.stdin.flush()

    def recibir(id_):
        for linea in p.stdout:
            m = json.loads(linea)
            if m.get('id') == id_:
                return m

    enviar({"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "live.py", "version": "1"}}})
    recibir(1)
    enviar({"jsonrpc": "2.0", "method": "notifications/initialized"})
    respuestas = []
    for i, (tool, args) in enumerate(llamadas, start=2):
        enviar({"jsonrpc": "2.0", "id": i, "method": "tools/call",
                "params": {"name": tool, "arguments": args}})
        r = recibir(i)
        respuestas.append(r)
        if 'error' in r or r.get('result', {}).get('isError'):
            break
    p.stdin.close()
    p.wait()
    return respuestas


if __name__ == '__main__':
    tool = sys.argv[1]
    if tool == 'batch-file':
        cmds = json.load(open(sys.argv[2]))['commands']
        r = llamar('batch', {"commands": cmds, "verbose": False, "timings": True})
    elif tool == 'replay':
        # paso a paso, para verlo construirse en la ventana
        cmds = json.load(open(sys.argv[2]))['commands']
        rs = sesion([('new_design', {"name": "soporte"})] +
                    [('execute', {"command": c['command'], "params": c.get('params', {}), "verbose": False})
                     for c in cmds])
        print(f'{len(rs) - 1} de {len(cmds)} pasos')
        r = rs[-1]
    else:
        r = llamar(tool, json.loads(sys.argv[2]) if len(sys.argv) > 2 else {})
    for c in r.get('result', {}).get('content', []):
        if c.get('type') == 'text':
            print(c['text'])
    if 'error' in r:
        print('ERROR', r['error'])
