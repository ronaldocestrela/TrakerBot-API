using FluentValidation;
using TrakerBot.Application.Bookmakers.DTOs;

namespace TrakerBot.Application.Bookmakers.Validators;

public class BaseBookmakerValidator<T, TDto> : AbstractValidator<T> where TDto : BaseBookmakerDto
{
    public BaseBookmakerValidator(Func<T, TDto> dtoSelector)
    {
        RuleFor(x => dtoSelector(x).Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters");
    }
}
