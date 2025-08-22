import os
import shutil
import tempfile

def clear_gen_py_cache():
    gen_py_dir = os.path.join(tempfile.gettempdir(), "gen_py")
    if os.path.exists(gen_py_dir):
        try:
            shutil.rmtree(gen_py_dir)
            print(f"🧹 Cleared COM cache: {gen_py_dir}")
        except Exception as e:
            print(f"⚠️  Failed to delete {gen_py_dir}: {e}")
    else:
        print(f"ℹ️  gen_py folder not found at: {gen_py_dir}")

'''
if __name__ == "__main__":
    clear_gen_py_cache()
'''