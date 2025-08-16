

export interface InputForm {
    label?: string
    placeholder?: string
    type?: string
    setValue: (value: any) => void
    value?: string | number
}
