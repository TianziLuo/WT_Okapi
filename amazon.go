package main

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"syscall"
	"unsafe"
)

func main() {
	targetDir := `C:\ACT\公用核心\下载_2.1 AMZ日报`
	sourceDir := `C:\ACT\RPA自动下载\AMZ_12345`

	// Step 1: clean target (.txt and .csv only) -> move to recycle bin
	entries, err := os.ReadDir(targetDir)
	if err != nil {
		fmt.Println("❌ Error reading target directory:", err)
		return
	}

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		ext := strings.ToLower(filepath.Ext(entry.Name()))
		if ext == ".txt" || ext == ".csv" {
			path := filepath.Join(targetDir, entry.Name())
			if err := moveToRecycleBin(path); err != nil {
				fmt.Println("❌ Failed to recycle:", path, "Error:", err)
			} else {
				fmt.Println("🗑 Moved to recycle:", path)
			}
		}
	}
	fmt.Println("✅ Target cleaned (one level only)")

	// Step 2: move special files
	moveAndDelete(sourceDir, targetDir, "（库龄）", "亚马逊物流库存（库龄）")
	moveAndDelete(sourceDir, targetDir, "费用预览", "费用预览")
	fmt.Println("✅ Special files moved")

	// Step 3: copy remaining files and clear source
	entries, err = os.ReadDir(sourceDir)
	if err != nil {
		fmt.Println("❌ Error reading source:", err)
		return
	}

	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		srcPath := filepath.Join(sourceDir, entry.Name())
		dstPath := filepath.Join(targetDir, entry.Name())

		if err := copyFile(srcPath, dstPath); err != nil {
			fmt.Println("❌ Copy failed:", srcPath, "->", dstPath, "Error:", err)
		} else {
			fmt.Println("✅ Copied:", srcPath, "->", dstPath)
			// move source file to recycle bin instead of delete
			if err := moveToRecycleBin(srcPath); err != nil {
				fmt.Println("❌ Failed to recycle source file:", srcPath, "Error:", err)
			} else {
				fmt.Println("🗑 Recycled source file:", srcPath)
			}
		}
	}

	fmt.Println("🎉 All done")
}

// move files with keyword from source to subfolder under target
func moveAndDelete(sourceDir, targetDir, keyword, subfolder string) {
	destDir := filepath.Join(targetDir, subfolder)
	_ = os.MkdirAll(destDir, os.ModePerm)

	entries, _ := os.ReadDir(sourceDir)
	for _, entry := range entries {
		if entry.IsDir() {
			continue
		}
		if strings.Contains(entry.Name(), keyword) {
			srcPath := filepath.Join(sourceDir, entry.Name())
			dstPath := filepath.Join(destDir, entry.Name())
			if err := os.Rename(srcPath, dstPath); err != nil {
				fmt.Println("❌ Failed to move:", srcPath, "->", dstPath, "Error:", err)
			} else {
				fmt.Println("✅ Moved:", srcPath, "->", dstPath)
			}
		}
	}
}

// copy one file from src to dst
func copyFile(src, dst string) error {
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	dstFile, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer dstFile.Close()

	_, err = io.Copy(dstFile, srcFile)
	return err
}

// moveToRecycleBin moves a file to Windows Recycle Bin using SHFileOperation
func moveToRecycleBin(path string) error {
	type SHFILEOPSTRUCT struct {
		Hwnd                  uintptr
		WFunc                 uint32
		PFrom                 *uint16
		PTo                   *uint16
		FFlags                uint16
		FAnyOperationsAborted int32
		HNameMappings         uintptr
		LpszProgressTitle     *uint16
	}

	const FO_DELETE = 3
	const FOF_ALLOWUNDO = 0x40
	const FOF_NOCONFIRMATION = 0x10

	from, err := syscall.UTF16PtrFromString(path + "\x00")
	if err != nil {
		return err
	}

	sh := SHFILEOPSTRUCT{
		Hwnd:   0,
		WFunc:  FO_DELETE,
		PFrom:  from,
		PTo:    nil,
		FFlags: FOF_ALLOWUNDO | FOF_NOCONFIRMATION,
	}

	r, _, err := syscall.NewLazyDLL("shell32.dll").NewProc("SHFileOperationW").Call(uintptr(unsafe.Pointer(&sh)))
	if r != 0 {
		return fmt.Errorf("SHFileOperation failed: %v", err)
	}
	return nil
}
