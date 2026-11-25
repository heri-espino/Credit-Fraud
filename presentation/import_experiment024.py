"""Import only the allowlisted aggregate report. No Kaggle submissions or OOF vectors."""
from pathlib import Path
import argparse, json, zipfile, csv, io, math
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'experiments'/'experiment026'/'resultados'
manifest=json.loads((DEST.parent/'manifest.json').read_text(encoding='utf8'))
def read_report(source):
    names=['figuras/'+n for n in manifest['figuras']]+manifest['agregados']
    if source.is_file():
        with zipfile.ZipFile(source) as z:
            possible=('informe_experiment024_es/','experiments/experiment026/resultados/','')
            prefix=next((p for p in possible if p+'resumen_final.json' in z.namelist()),None)
            if prefix is None: raise ValueError('No se encontró resumen_final.json')
            return {n:z.read(prefix+n) for n in names}
    if source.name=='figuras': source=source.parent
    if (source/'informe_experiment024_es').is_dir(): source=source/'informe_experiment024_es'
    return {n:(source/n).read_bytes() for n in names}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    args=parser.parse_args()
    data=read_report(args.source)
    summary=json.loads(data['resumen_final.json'])
    if summary['protocolo']!=manifest['protocolo'] or summary['firma']!=manifest['firma']:
        raise ValueError('El informe no corresponde a la corrida documentada.')
    rows=list(csv.DictReader(io.StringIO(data['top10.csv'].decode('utf-8-sig'))))
    expected=list(csv.DictReader((DEST/'top10.csv').read_text(encoding='utf8').splitlines()))
    if rows!=expected or len(rows)!=10 or rows[0]['familia']!=summary['seleccion_nominal']:
        raise ValueError('Top 10 distinto del resultado versionado.')
    if not math.isclose(float(rows[0]['roc_auc']),summary['auc_seleccionado'],rel_tol=0,abs_tol=1e-12):
        raise ValueError('AUC incompatible.')
    for n in manifest['figuras']:
        if not data['figuras/'+n].startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('PNG inválido: '+n)
    for name,content in data.items():
        # Keep canonical committed CSV and JSON formatting unchanged.
        if name in ('top10.csv','resumen_final.json'): continue
        target=DEST/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(content)
    print(f'Verificados {len(manifest["figuras"])} PNG y {len(manifest["agregados"])} agregados en {DEST}.')
    print('No se importó envio_final_kaggle.csv ni ningún vector individual.')
if __name__=='__main__': main()
